from flask_restful import Resource, reqparse
from models import db, Review

class ReviewResource(Resource):
    def get(self, review_id=None):
        if review_id:
            review = Review.query.get_or_404(review_id)
            return review.to_dict()  # This will now work because to_dict() is defined in the model
        else:
            reviews = Review.query.all()
            return [review.to_dict() for review in reviews]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', required=True, type=int, help="Rating cannot be blank!")
        parser.add_argument('comment', required=False)
        parser.add_argument('recipe_id', required=True, type=int, help="Recipe ID cannot be blank!")
        parser.add_argument('user_id', required=True, type=int, help="User ID cannot be blank!")
        args = parser.parse_args()

        new_review = Review(
            rating=args['rating'],
            comment=args['comment'],
            recipe_id=args['recipe_id'],
            user_id=args['user_id']
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review.to_dict(), 201  # Now works as expected

    def put(self, review_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', required=True, type=int, help="Rating cannot be blank!")
        parser.add_argument('comment', required=False)
        parser.add_argument('recipe_id', required=True, type=int, help="Recipe ID cannot be blank!")
        parser.add_argument('user_id', required=True, type=int, help="User ID cannot be blank!")
        args = parser.parse_args()

        review = Review.query.get_or_404(review_id)
        review.rating = args['rating']
        review.comment = args['comment']
        review.recipe_id = args['recipe_id']
        review.user_id = args['user_id']
        db.session.commit()
        return review.to_dict()  # This will return the updated review

    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return '', 204  # Return empty response for successful deletion
