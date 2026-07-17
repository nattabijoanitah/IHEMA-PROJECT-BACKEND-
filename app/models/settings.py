from datetime import datetime

from app.extensions import db



class Media(db.Model):

    """
    Every uploaded file is tracked here.
    """

    __tablename__ = "media"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    filename = db.Column(
        db.String(255),
        nullable=False
    )


    url = db.Column(
        db.String(255),
        nullable=False
    )


    media_type = db.Column(

        db.Enum(
            "image",
            "video",
            name="media_type"
        ),

        nullable=False

    )


    uploaded_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )


    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    def to_dict(self):

        return {

            "id": self.id,

            "filename": self.filename,

            "url": self.url,

            "media_type": self.media_type,

            "uploaded_at":
            (
                self.uploaded_at.isoformat()
                if self.uploaded_at
                else None
            )

        }





class SiteSettings(db.Model):

    """
    Singleton row holding site branding.
    """

    __tablename__ = "site_settings"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    site_name = db.Column(
        db.String(120),
        default="My Website"
    )


    logo_url = db.Column(
        db.String(255)
    )


    favicon_url = db.Column(
        db.String(255)
    )


    primary_color = db.Column(
        db.String(20),
        default="#1E40AF"
    )


    secondary_color = db.Column(
        db.String(20),
        default="#F59E0B"
    )


    accent_color = db.Column(
        db.String(20),
        default="#10B981"
    )


    background_color = db.Column(
        db.String(20),
        default="#FFFFFF"
    )


    text_color = db.Column(
        db.String(20),
        default="#111827"
    )


    font_family = db.Column(
        db.String(100),
        default="Inter, sans-serif"
    )


    footer_text = db.Column(
        db.String(255)
    )


    contact_email = db.Column(
        db.String(120)
    )


    contact_phone = db.Column(
        db.String(50)
    )


    address = db.Column(
        db.String(255)
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    def to_dict(self):

        return {

            "site_name": self.site_name,

            "logo_url": self.logo_url,

            "favicon_url": self.favicon_url,

            "theme": {

                "primary_color": self.primary_color,

                "secondary_color": self.secondary_color,

                "accent_color": self.accent_color,

                "background_color": self.background_color,

                "text_color": self.text_color,

                "font_family": self.font_family

            },

            "footer_text": self.footer_text,

            "contact_email": self.contact_email,

            "contact_phone": self.contact_phone,

            "address": self.address

        }