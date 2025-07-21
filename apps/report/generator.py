from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    KeepTogether,
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import calendar
from datetime import date, datetime, timedelta
import random

from apps.catalog.models import Book
from apps.loan.models import Loan

month_names = {
    1: "JANUARI",
    2: "FEBRUARI",
    3: "MARET",
    4: "APRIL",
    5: "MEI",
    6: "JUNI",
    7: "JULI",
    8: "AGUSTUS",
    9: "SEPTEMBER",
    10: "OKTOBER",
    11: "NOVEMBER",
    12: "DESEMBER",
}


classifications = [
    "000 Karya Umum",
    "100 Filsafat",
    "200 Agama",
    "300 Ilmu-ilmu Sosial",
    "400 Bahasa",
    "500 Ilmu Murni",
    "600 Teknologi Terapan",
    "700 Kesenian & Olahraga",
    "800 Kesusasteraan",
    "900 Sejarah, Biografi & Geografi",
    "F Fiksi",
    "Referensi",
    "Audio Visual",
]


class LibraryReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            "CustomTitle",
            parent=self.styles["Heading1"],
            fontSize=14,
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        )

        self.heading_style = ParagraphStyle(
            "CustomHeading",
            parent=self.styles["Heading2"],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=12,
            fontName="Helvetica-Bold",
        )

        self.normal_style = ParagraphStyle(
            "CustomNormal", parent=self.styles["Normal"], fontSize=12, spaceAfter=3
        )

    def get_month_name_id(self, month):
        """Get Indonesian month name"""
        return month_names.get(month, "UNKNOWN")

    def _get_classification_from_category(self, category_name):
        """Maps a book category name to its broader classification."""
        try:
            # Handle numeric classifications (e.g., "540" -> "500 Ilmu Murni")
            numeric_category = int(category_name)
            if 0 <= numeric_category < 100:
                return "000 Karya Umum"
            elif 100 <= numeric_category < 200:
                return "100 Filsafat"
            elif 200 <= numeric_category < 300:
                return "200 Agama"
            elif 300 <= numeric_category < 400:
                return "300 Ilmu-ilmu Sosial"
            elif 400 <= numeric_category < 500:
                return "400 Bahasa"
            elif 500 <= numeric_category < 600:
                return "500 Ilmu Murni"
            elif 600 <= numeric_category < 700:
                return "600 Teknologi Terapan"
            elif 700 <= numeric_category < 800:
                return "700 Kesenian & Olahraga"
            elif 800 <= numeric_category < 900:
                return "800 Kesusasteraan"
            elif 900 <= numeric_category < 1000:
                return "900 Sejarah, Biografi & Geografi"
            else:
                return "Lain-lain"  # Or handle unknown numeric categories as needed
        except ValueError:
            # Handle non-numeric classifications (e.g., "F" -> "F Fiksi")
            if category_name == "F":
                return "F Fiksi"
            elif category_name == "Referensi":
                return "Referensi"
            elif category_name == "Audio Visual":
                return "Audio Visual"
            else:
                return "Lain-lain"  # Default for unknown non-numeric categories

    def calculate_working_days(self, month, year):
        """Calculate working days (Monday-Friday) in the month"""
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])

        working_days = 0
        current_date = first_day
        while current_date <= last_day:
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                working_days += 1
            current_date += timedelta(days=1)
        return working_days

    def generate_loan_data(self, month, year):
        """
        Generates loan data for a specific month and year,
        categorized by classification, using actual Django Loan data.
        """
        # Fetch all relevant loans for the given month and year
        # Use select_related to efficiently retrieve related Book and Category objects
        loans_in_month = (
            Loan.objects.filter(loan_date__year=year, loan_date__month=month)
            .select_related("book")
            .prefetch_related("book__category")
        )

        # Initialize dictionaries to hold counts for each classification
        classification_titles = {cls: set() for cls in classifications}
        classification_titles["Lain-lain"] = (
            set()
        )  # To store unique titles (by ID or title string)

        classification_copies = {cls: 0 for cls in classifications}
        classification_copies["Lain-lain"] = (
            0  # To store total loan instances (copies loaned)
        )

        for loan_instance in loans_in_month:
            book = loan_instance.book

            # Ensure book and its category exist
            if book and book.category:
                # Assuming 'category' is a ForeignKey to a Category model
                # and Category model has a 'name' field
                category_name = book.category.first().name
                classification = self._get_classification_from_category(category_name)

                # Add book to the set of unique titles for its classification
                # Use book.id for uniqueness if possible, otherwise book.title
                if classification in classification_titles:
                    classification_titles[classification].add(
                        book.id
                    )  # Use book.id for true uniqueness
                    classification_copies[classification] += 1
                else:
                    # Handle 'Lain-lain' for unmapped categories
                    classification_titles["Lain-lain"].add(book.id)
                    classification_copies["Lain-lain"] += 1

        # Prepare the data for display and calculate totals
        data = []
        total_unique_titles = 0
        total_loaned_copies = 0

        for i, classification_name in enumerate(classifications, 1):
            titles_count = len(classification_titles[classification_name])
            copies_count = classification_copies[classification_name]
            data.append(
                [str(i), classification_name, str(titles_count), str(copies_count)]
            )
            total_unique_titles += titles_count
            total_loaned_copies += copies_count

        # Add "Lain-lain" if there were any unmapped categories
        lain_lain_titles_count = len(classification_titles["Lain-lain"])
        lain_lain_copies_count = classification_copies["Lain-lain"]

        if lain_lain_titles_count > 0 or lain_lain_copies_count > 0:
            data.append(
                [
                    str(len(classifications) + 1),
                    "Lain-lain",
                    str(lain_lain_titles_count),
                    str(lain_lain_copies_count),
                ]
            )
            total_unique_titles += lain_lain_titles_count
            total_loaned_copies += lain_lain_copies_count

        data.append(["", "Jumlah", str(total_unique_titles), str(total_loaned_copies)])
        return data, total_unique_titles, total_loaned_copies

    def generate_member_data(self):
        today = date(2025, 7, 18)  # Hardcoded for demonstration based on current date
        simulated_members = [
            ("Alice Smith", "Batch 2023", "2026-01-15"),  # Active
            ("Bob Johnson", "Batch 2024", "2025-06-30"),  # Expired
            ("Charlie Brown", "Batch 2023", "2025-12-01"),  # Active
            ("Diana Prince", "Batch 2025", "2027-03-20"),  # Active
            ("Eve Adams", "Batch 2024", "2025-08-10"),  # Active
            ("Frank Green", "Batch 2023", "2024-11-20"),  # Expired
            ("Grace Lee", "Batch 2025", "2025-07-17"),  # Expired (yesterday)
        ]
        batch_data = {}
        for name, batch, expiry_str in simulated_members:
            if batch not in batch_data:
                batch_data[batch] = {"members": [], "active_count": 0, "total_count": 0}

            expiry_date = date.fromisoformat(
                expiry_str
            )  # Convert string to date object
            is_active = expiry_date >= today  # Check if active

            batch_data[batch]["members"].append({"name": name, "is_active": is_active})
            batch_data[batch]["total_count"] += 1
            if is_active:
                batch_data[batch]["active_count"] += 1

        # Prepare data for the table
        table_data = []

        # Add global header row
        table_data.append(["Angkatan", "Total Anggota", "Anggota Aktif"])

        total_overall_members = 0
        total_overall_active = 0

        # Sort batches for consistent report generation
        sorted_batches = sorted(batch_data.keys())

        for batch_name in sorted_batches:
            data = batch_data[batch_name]
            total_batch_members = data["total_count"]
            active_batch_members = data["active_count"]

            table_data.append(
                [
                    Paragraph(batch_name),  # Batch name in bold
                    str(total_batch_members),
                    str(active_batch_members),
                ]
            )

            total_overall_members += total_batch_members
            total_overall_active += active_batch_members

        # Add a row for the grand total
        table_data.append(
            [
                Paragraph(
                    "<b>TOTAL KESELURUHAN ANGGOTA</b>",
                ),
                str(total_overall_members),
                str(total_overall_active),
            ]
        )

        return table_data, total_overall_members

    # --- NEW: generate_collection_data ---
    def generate_collection_data(self, month, year):
        """
        Generates collection addition data for a specific month and year,
        categorized by classification, using actual Django Book data.
        """
        # Books are considered newly added if their 'created_at' date falls within
        # the specified month and year.
        # Use prefetch_related for ManyToManyField 'category'
        newly_added_books = Book.objects.filter(
            created_at__year=year, created_at__month=month
        ).prefetch_related("category")

        # Initialize dictionaries to hold counts for each classification
        # titles: count of unique book titles newly added
        # copies: sum of 'stock' for newly added books
        classification_counts = {
            cls: {"titles": 0, "copies": 0} for cls in classifications
        }
        classification_counts["Lain-lain"] = {"titles": 0, "copies": 0}

        for book_instance in newly_added_books:
            # A book can have multiple categories, so we need to iterate or decide on a primary
            # For this report, we'll try to map it to the first category, or 'Lain-lain' if none
            if book_instance.category.exists():
                # Get the name of the first category for classification
                category_name = book_instance.category.first().name
                classification = self._get_classification_from_category(category_name)
            else:
                classification = "Lain-lain"  # No category assigned

            # Increment counts for the determined classification
            if classification in classification_counts:
                classification_counts[classification]["titles"] += 1
                classification_counts[classification]["copies"] += book_instance.stock
            else:
                # This should ideally not happen if 'Lain-lain' is handled, but as a fallback
                classification_counts["Lain-lain"]["titles"] += 1
                classification_counts["Lain-lain"]["copies"] += book_instance.stock

        # Prepare the data for display and calculate totals
        data = []
        total_titles = 0
        total_copies = 0

        for i, classification_name in enumerate(classifications, 1):
            titles = classification_counts[classification_name]["titles"]
            copies = classification_counts[classification_name]["copies"]
            data.append([str(i), classification_name, str(titles), str(copies)])
            total_titles += titles
            total_copies += copies

        # Add "Lain-lain" if there were any unmapped categories or books without categories
        lain_lain_titles = classification_counts["Lain-lain"]["titles"]
        lain_lain_copies = classification_counts["Lain-lain"]["copies"]

        if lain_lain_titles > 0 or lain_lain_copies > 0:
            data.append(
                [
                    str(len(classifications) + 1),
                    "Lain-lain",
                    str(lain_lain_titles),
                    str(lain_lain_copies),
                ]
            )
            total_titles += lain_lain_titles
            total_copies += lain_lain_copies

        data.append(["", "Jumlah", str(total_titles), str(total_copies)])
        return data, total_titles, total_copies

    def generate_report(self, month, year, filename=None):
        """Generate the complete PDF report"""
        if filename is None:
            month_name = self.get_month_name_id(month).capitalize()
            filename = f"Laporan_Perpustakaan_{month_name}_{year}.pdf"

        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        story = []

        # Title
        title = Paragraph("LAPORAN KEGIATAN PERPUSTAKAAN", self.title_style)
        subtitle1 = Paragraph(
            f"BULAN {self.get_month_name_id(month)} {year}", self.title_style
        )
        subtitle2 = Paragraph("PERPUSTAKAAN SMAN 3 BANJARMASIN", self.title_style)

        story.append(title)
        story.append(subtitle1)
        story.append(subtitle2)
        story.append(Spacer(1, 20))

        # Section A: Service Activities
        story.append(Paragraph("A. KEGIATAN LAYANAN", self.heading_style))

        working_days = self.calculate_working_days(month, year)
        service_data = [
            ["Jumlah Hari", ":", f"{working_days} Hari"],
            ["Waktu Layanan", ":", "Senin - Jum'at 08.00 - 16.00 WITA"],
            ["Jumlah Staf Perpustakaan", ":", "2 Orang"],
        ]

        service_table = Table(service_data, colWidths=[3 * inch, 0.3 * inch, 2 * inch])
        service_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        story.append(service_table)
        story.append(Spacer(1, 15))

        # # Section B: Monthly Visitors
        # story.append(
        #     Paragraph(
        #         "A. JUMLAH PENGUNJUNG BULANAN YANG DILAPORKAN", self.heading_style
        #     )
        # )
        #
        # visitor_data, total_visitors = self.generate_visitor_data()
        # visitor_headers = [["No.", "Pengunjung Perpustakaan", "Jumlah Perbulan"]]
        # visitor_table_data = visitor_headers + visitor_data
        #
        # visitor_table = Table(
        #     visitor_table_data, colWidths=[0.5 * inch, 3 * inch, 1.5 * inch]
        # )
        # visitor_table.setStyle(
        #     TableStyle(
        #         [
        #             ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        #             ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        #             ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        #             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        #             ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        #             ("FONTSIZE", (0, 0), (-1, -1), 9),
        #             ("GRID", (0, 0), (-1, -1), 1, colors.black),
        #             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        #             ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
        #             ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        #         ]
        #     )
        # )
        # story.append(visitor_table)
        # story.append(Spacer(1, 15))

        # Section b: Total Members
        section_b_title = Paragraph("B. JUMLAH ANGGOTA", self.heading_style)

        member_data, total_members = self.generate_member_data()

        member_table = Table(member_data, colWidths=[3 * inch, 1.5 * inch])
        member_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ]
            )
        )
        story.append(KeepTogether([section_b_title, member_table]))
        story.append(Spacer(1, 15))

        # Section C: Monthly Loans
        story.append(
            Paragraph(
                f"C. JUMLAH PEMINJAMAN BULAN {self.get_month_name_id(month)}",
                self.heading_style,
            )
        )

        loan_data, total_titles, total_copies = self.generate_loan_data(month, year)
        loan_headers = [["No.", "Klasifikasi", "Judul", "Eksemplar"]]
        loan_table_data = loan_headers + loan_data

        loan_table = Table(loan_table_data)
        loan_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ]
            )
        )
        story.append(loan_table)
        story.append(Spacer(1, 10))

        # Section D: Collection Addition
        section_d_title = Paragraph("D. PENAMBAHAN KOLEKSI", self.heading_style)

        collection_data, _, _ = self.generate_collection_data(month, year)
        collection_headers = [
            [
                "No.",
                "Klasifikasi",
                "Judul",
                "Eksemplar",
            ]
        ]
        collection_table_data = collection_headers + collection_data

        collection_table = Table(collection_table_data)
        collection_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ]
            )
        )
        story.append(KeepTogether([section_d_title, collection_table]))
        story.append(Spacer(1, 30))

        # Signature Section
        last_day = calendar.monthrange(year, month)[1]
        signature_text = f"Banjarmasin, {last_day} {self.get_month_name_id(month).capitalize()} {year}"
        story.append(
            Paragraph(
                signature_text,
                ParagraphStyle("RightAlign", parent=self.normal_style, alignment=2),
            )
        )
        story.append(Spacer(1, 15))

        # Signature table
        signature_data = [
            ["Mengetahui,", ""],
            ["Kepala SMAN 3 Banjarmasin", "Kepala Perpustakaan"],
            ["", ""],
            ["", ""],
            ["", ""],
            ["H. Zaini Juhdi, S.Pd, M.M", "Bahtiar, M.Pd"],
            ["NIP. 19650902 199003 1 010", "NIP. 19771015 200904 1 002"],
        ]
        page_width = A4[0]  # Get width from page size tuple
        left_margin = 2 * cm
        right_margin = 2 * cm
        available_width = page_width - left_margin - right_margin

        column_width = available_width / 2

        signature_table = Table(signature_data, colWidths=[column_width, column_width])
        signature_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    # Align the second column (index 1) to the RIGHT
                    ("ALIGN", (1, 0), (1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    # ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                    ("FONTNAME", (0, 5), (-1, 6), "Helvetica-Bold"),
                ]
            )
        )
        story.append(signature_table)

        # Build PDF
        doc.build(story)
        print(f"PDF report generated: {filename}")
        return filename


# Usage functions
def generate_library_report_pdf(month, year, filename=None):
    """
    Generate a PDF library report for the specified month and year

    Args:
        month (int): Month number (1-12)
        year (int): Year (e.g., 2024)
        filename (str, optional): Output filename. If None, auto-generates

    Returns:
        str: Path to the generated PDF file
    """
    generator = LibraryReportGenerator()
    return generator.generate_report(month, year, filename)


# Example usage
if __name__ == "__main__":
    # Generate report for May 2024
    print("Generating library report for May 2024...")
    pdf_file = generate_library_report_pdf(5, 2024)
    print(f"Report saved as: {pdf_file}")

    # Generate report for current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    print(f"\nGenerating library report for {current_month}/{current_year}...")
    pdf_file2 = generate_library_report_pdf(current_month, current_year)
    print(f"Report saved as: {pdf_file2}")
