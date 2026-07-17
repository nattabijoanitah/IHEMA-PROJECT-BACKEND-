from datetime import datetime

from app.extensions import db



class Page(db.Model):

    """
    A single page of the site.
    Home, About Us, Services, Contact.
    """

    __tablename__ = "pages"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(150),
        nullable=False
    )


    slug = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )


    meta_title = db.Column(
        db.String(160)
    )


    meta_description = db.Column(
        db.String(300)
    )


    is_published = db.Column(
        db.Boolean,
        default=False
    )


    is_homepage = db.Column(
        db.Boolean,
        default=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    hero_sections = db.relationship(
        "HeroSection",
        back_populates="page",
        cascade="all, delete-orphan",
        order_by="HeroSection.order"
    )


    content_sections = db.relationship(
        "ContentSection",
        back_populates="page",
        cascade="all, delete-orphan",
        order_by="ContentSection.order"
    )



    def to_dict(self, with_children=False):

        data = {

            "id": self.id,

            "title": self.title,

            "slug": self.slug,

            "meta_title": self.meta_title,

            "meta_description": self.meta_description,

            "is_published": self.is_published,

            "is_homepage": self.is_homepage

        }


        if with_children:

            data["hero_sections"] = [
                h.to_dict()
                for h in self.hero_sections
            ]


            data["content_sections"] = [
                c.to_dict(with_blocks=True)
                for c in self.content_sections
            ]


        return data