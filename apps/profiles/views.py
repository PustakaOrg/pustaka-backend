import pandas as pd
from rest_framework import viewsets, status, response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import transaction

from apps.authentication.serializers import UserSerializer
from apps.authentication.models import User
from apps.profiles.filters import BatchFilter, ClassFilter, MemberFilter
from core.permissions import (
    IsAdminOrLibrarianModify,
    IsAdminOrLibrarianOrOwner,
    IsAdminOrOwner,
)

from .models import Batch, Class, Member, Librarian
from .serializers import (
    BatchSerializer,
    ClassSerializer,
    MemberSerializer,
    LibrarianSerializer,
)


class LibrarianViewSet(viewsets.ModelViewSet):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    permission_classes = [IsAdminOrOwner]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminOrLibrarianOrOwner]
    filterset_class = MemberFilter

    @action(detail=False, methods=["post"], url_path="import")
    def import_books(self, request):
        if "file" not in request.FILES:
            return response.Response(
                {"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        csv_file = request.FILES["file"]

        if not csv_file.name.endswith(".csv"):
            return response.Response(
                {"detail": "File is not a CSV."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_csv(csv_file)

            created_count = 0
            skipped_count = 0
            error_rows = []

            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        nis = str(row["NIS"]).strip()

                        if Member.objects.filter(nis=nis).exists():
                            skipped_count += 1
                            continue

                        user = User.objects.create_member_user(
                            fullname=row["Nama"],
                            email=row["Email"],
                            password=row["Password"],
                        )

                        _class, _ = Class.objects.get_or_create(name=row["Kelas"])
                        batch, _ = Batch.objects.get_or_create(name=row["Angkatan"])

                        phone_number = (
                            str(row.get("No HP")).strip()
                            if pd.notna(row.get("No HP"))
                            and str(row.get("No HP")).strip()
                            else None
                        )

                        Member.objects.create(
                            account=user,
                            nis=nis,
                            _class=_class,
                            batch=batch,
                            phone_number=phone_number,
                        )

                        created_count += 1

                    except Exception as e:
                        error_rows.append({"row_index": index, "error": str(e)})
                        skipped_count += 1

            return response.Response(
                {
                    "detail": "Import completed.",
                    "created": created_count,
                    "skipped": skipped_count,
                    "errors": error_rows,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return response.Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = ClassFilter


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = BatchFilter


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    try:
        member = user.member
        context = {"request": request}
        serializer = MemberSerializer(member, context=context)
        return Response(serializer.data)
    except Member.DoesNotExist:
        pass

    try:
        librarian = user.librarian
        serializer = LibrarianSerializer(librarian)
        return Response(serializer.data)
    except Librarian.DoesNotExist:
        pass

    # Check if the user is an Admin
    if user.groups.filter(
        name="Admin"
    ).exists():  # Assuming admin users are marked as staff
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=200)

    # If the user is neither a Member, Librarian, nor Admin
    return Response({"detail": "User profile not found."}, status=404)
