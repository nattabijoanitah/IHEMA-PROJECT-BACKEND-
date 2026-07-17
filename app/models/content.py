from app.extensions import db



class ContentSection(db.Model):

    """
    A block-group on a page.
    """

    __tablename__ = "content_sections"



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
        back_populates="content_sections"
    )


    title = db.Column(
        db.String(150)
    )


    layout = db.Column(
        db.String(50),
        default="default"
    )


    order = db.Column(
        db.Integer,
        default=0
    )


    is_active = db.Column(
        db.Boolean,
        default=True
    )



    blocks = db.relationship(

        "ContentBlock",

        back_populates="section",

        cascade="all, delete-orphan",

        order_by="ContentBlock.order"

    )



    def to_dict(self, with_blocks=False):

        data = {

            "id": self.id,

            "page_id": self.page_id,

            "title": self.title,

            "layout": self.layout,

            "order": self.order,

            "is_active": self.is_active

        }


        if with_blocks:

            data["blocks"] = [

                b.to_dict()

                for b in self.blocks

            ]


        return data





class ContentBlock(db.Model):

    """
    A single piece of content.
    """

    __tablename__ = "content_blocks"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    section_id = db.Column(
        db.Integer,
        db.ForeignKey("content_sections.id"),
        nullable=False
    )


    section = db.relationship(
        "ContentSection",
        back_populates="blocks"
    )


    block_type = db.Column(

        db.Enum(
            "heading",
            "paragraph",
            "image",
            "video",
            name="content_block_type"
        ),

        nullable=False

    )


    text_content = db.Column(
        db.Text
    )


    media_url = db.Column(
        db.String(255)
    )


    media_caption = db.Column(
        db.String(255)
    )


    order = db.Column(
        db.Integer,
        default=0
    )



    def to_dict(self):

        return {

            "id": self.id,

            "section_id": self.section_id,

            "block_type": self.block_type,

            "text_content": self.text_content,

            "media_url": self.media_url,

            "media_caption": self.media_caption,

            "order": self.order

        }