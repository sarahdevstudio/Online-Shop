class Review:

    def __init__(
        self,
        id,
        product_id,
        user_id,
        rating,
        comment,
        created_at
    ):
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
