from app.extensions import db



class MenuItem(db.Model):

    """
    A single navbar link.
    Supports nested dropdowns using parent_id.
    """

    __tablename__ = "menu_items"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    label = db.Column(
        db.String(80),
        nullable=False
    )


    page_id = db.Column(
        db.Integer,
        db.ForeignKey("pages.id"),
        nullable=True
    )


    page = db.relationship(
        "Page"
    )


    custom_url = db.Column(
        db.String(255),
        nullable=True
    )


    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("menu_items.id"),
        nullable=True
    )


    children = db.relationship(
        "MenuItem",
        backref=db.backref(
            "parent",
            remote_side=[id]
        )
    )


    order = db.Column(
        db.Integer,
        default=0
    )


    is_active = db.Column(
        db.Boolean,
        default=True
    )


    open_in_new_tab = db.Column(
        db.Boolean,
        default=False
    )



    def resolved_url(self):

        if self.page:

            return (
                f"/{self.page.slug}"
                if not self.page.is_homepage
                else "/"
            )

        return self.custom_url or "#"



    def to_dict(self, with_children=True):

        data = {

            "id": self.id,

            "label": self.label,

            "url": self.resolved_url(),

            "order": self.order,

            "is_active": self.is_active,

            "open_in_new_tab": self.open_in_new_tab

        }


        if with_children:

            data["children"] = [

                c.to_dict()

                for c in sorted(
                    self.children,
                    key=lambda x: x.order
                )

            ]


        return data