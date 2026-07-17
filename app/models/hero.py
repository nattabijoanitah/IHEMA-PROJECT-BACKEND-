from app.extensions import db



class HeroSection(db.Model):

    """
    Top banner of a page.
    """

    __tablename__ = "hero_sections"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    page_id = db.Column(
        db.Integer,
        db.ForeignKey("pages.id"),
        nullable=False
    )


    page = db.relationship(
        "Page",
        back_populates="hero_sections"
    )


    heading = db.Column(
        db.String(200)
    )


    subheading = db.Column(
        db.String(300)
    )


    media_type = db.Column(
        db.Enum(
            "image",
            "video",
            name="hero_media_type"
        ),
        default="image"
    )


    media_url = db.Column(
        db.String(255)
    )


    cta_text = db.Column(
        db.String(80)
    )


    cta_url = db.Column(
        db.String(255)
    )


    order = db.Column(
        db.Integer,
        default=0
    )


    is_active = db.Column(
        db.Boolean,
        default=True
    )



    def to_dict(self):

        return {

            "id": self.id,

            "page_id": self.page_id,

            "heading": self.heading,

            "subheading": self.subheading,

            "media_type": self.media_type,

            "media_url": self.media_url,

            "cta_text": self.cta_text,

            "cta_url": self.cta_url,

            "order": self.order,

            "is_active": self.is_active

        }