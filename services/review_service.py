from datetime import datetime

from models.review import Review
from utils.file_manager import FileManager


class ReviewService:

    REVIEWS_FILE = "data/reviews.txt"

    MIN_RATING = 1
    MAX_RATING = 5

    @staticmethod
    def get_reviews():

        reviews = []

        lines = FileManager.read_file(
            ReviewService.REVIEWS_FILE
        )

        for line in lines:

            line = line.strip()

            if not line:
                continue

            data = line.split("|", 5)

            if len(data) != 6:
                continue

            try:

                review = Review(
                    int(data[0]),
                    int(data[1]),
                    int(data[2]),
                    int(data[3]),
                    data[4],
                    data[5]
                )

                reviews.append(review)

            except ValueError:
                continue

        return reviews

    @staticmethod
    def save_reviews(reviews):

        data = []

        for review in reviews:

            line = (
                f"{review.id}|"
                f"{review.product_id}|"
                f"{review.user_id}|"
                f"{review.rating}|"
                f"{review.comment}|"
                f"{review.created_at}\n"
            )

            data.append(line)

        FileManager.update_file(
            ReviewService.REVIEWS_FILE,
            data
        )

    @staticmethod
    def get_product_reviews(product_id):

        return [
            review
            for review in ReviewService.get_reviews()
            if review.product_id == product_id
        ]

    @staticmethod
    def get_rating_summary(product_id):

        reviews = ReviewService.get_product_reviews(product_id)

        if not reviews:
            return None, 0

        average = sum(
            review.rating for review in reviews
        ) / len(reviews)

        return average, len(reviews)

    @staticmethod
    def has_purchased(user_id, product_id):

        # imported here to avoid a circular import
        from services.order_service import OrderService
        from services.report_service import ReportService

        for order in OrderService.get_user_orders(user_id):

            if order.status != "Completed":
                continue

            for item_id, _ in ReportService.parse_order_items(order):

                if item_id == product_id:
                    return True

        return False

    @staticmethod
    def add_review(user_id, product_id, rating, comment):

        if not (
            ReviewService.MIN_RATING
            <= rating
            <= ReviewService.MAX_RATING
        ):
            return False, "Rating must be between 1 and 5."

        if not ReviewService.has_purchased(user_id, product_id):
            return False, (
                "You can only review products from "
                "your completed orders."
            )

        reviews = ReviewService.get_reviews()

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # one review per user per product: a new one replaces the old
        for review in reviews:

            if (
                review.user_id == user_id
                and review.product_id == product_id
            ):

                review.rating = rating
                review.comment = comment
                review.created_at = created_at

                ReviewService.save_reviews(reviews)

                return True, "Your review has been updated."

        new_id = 1

        if reviews:
            new_id = max(review.id for review in reviews) + 1

        reviews.append(
            Review(
                new_id,
                product_id,
                user_id,
                rating,
                comment,
                created_at
            )
        )

        ReviewService.save_reviews(reviews)

        return True, "Thank you for your review!"

    @staticmethod
    def delete_product_reviews(product_id):

        reviews = [
            review
            for review in ReviewService.get_reviews()
            if review.product_id != product_id
        ]

        ReviewService.save_reviews(reviews)

    @staticmethod
    def display_product_reviews(product_id):

        # imported here to avoid a circular import
        from services.auth_service import AuthService

        reviews = ReviewService.get_product_reviews(product_id)

        if not reviews:

            print("\nNo reviews for this product yet.")
            return

        average, count = ReviewService.get_rating_summary(
            product_id
        )

        print(
            f"\n========== REVIEWS "
            f"({average:.1f}/5 from {count}) =========="
        )

        for review in reviews:

            user = AuthService.get_user_by_id(review.user_id)

            author = user.username if user else "Deleted user"

            print(
                f"\n{'*' * review.rating}"
                f"{'-' * (ReviewService.MAX_RATING - review.rating)}"
                f"  {author}  ({review.created_at})"
            )

            if review.comment:
                print(review.comment)
