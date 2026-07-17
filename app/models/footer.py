from app.extensions import db



class FooterColumn(db.Model):

    """
    A group of links in the footer.
    """

    __tablename__ = "footer_columns"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(100),
        nullable=False
    )


    order = db.Column(
        db.Integer,
        default=0
    )



    links = db.relationship(

        "FooterLink",

        back_populates="column",

        cascade="all, delete-orphan",

        order_by="FooterLink.order"

    )



    def to_dict(self):

        return {

            "id": self.id,

            "title": self.title,

            "order": self.order,

            "links": [

                l.to_dict()

                for l in self.links

            ]

        }





class FooterLink(db.Model):

    __tablename__ = "footer_links"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    column_id = db.Column(
        db.Integer,
        db.ForeignKey("footer_columns.id"),
        nullable=False
    )


    column = db.relationship(
        "FooterColumn",
        back_populates="links"
    )


    label = db.Column(
        db.String(100),
        nullable=False
    )


    url = db.Column(
        db.String(255),
        nullable=False
    )


    order = db.Column(
        db.Integer,
        default=0
    )



    def to_dict(self):

        return {

            "id": self.id,

            "label": self.label,

            "url": self.url,

            "order": self.order

        }





class SocialLink(db.Model):

    """
    Footer social icons.
    """

    __tablename__ = "social_links"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    platform = db.Column(
        db.String(50),
        nullable=False
    )


    url = db.Column(
        db.String(255),
        nullable=False
    )


    order = db.Column(
        db.Integer,
        default=0
    )



    def to_dict(self):

        return {

            "id": self.id,

            "platform": self.platform,

            "url": self.url,

            "order": self.order

        }