from apps.settings.models import Settings


def generate_member_card(members):
    settings = Settings.get_instance()
    background_img_url = settings.member_card_background
    pass


def generate_book_sticker(books):
    pass
