class Moviemon:
    def __init__(self, mov_id):
        """
        TODO: id를 imdb api로 가져와 영화이름, 포스터 이미지 주소, 힘(평점) 저장하기
        """
        assert mov_id  # id가 없을시 오류
        self.id = mov_id
        self.name = "TBD"
        self.poster = "TBD"
        self.strength = "TBD"
