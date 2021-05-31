class Moviemon:
    def __init__(
        self,
        title="대충 멋있는 제목",
        year="네자리 수",
        director="대충 쩌는 감독",
        poster="대충 쿨한 이미지 링크",
        rating="평점",
        plot="대충 쩌는 내용",
        actors="대충 개멋있는 배우",
    ):  # 빈 입력일시 기본값
        """
        무비몬의 모든 정보를 저장. 사용 방법:
        the_host = Moviemon(<영화 id>, <영화이름>("괴물"), <포스터 이미지 주소>, <평점>("4.5"))
        """
        self.title = title
        self.year = year
        self.director = director
        self.poster = poster
        self.rating = rating
        self.plot = plot
        self.actors = actors

    def __str__(self):
        return self.title  # 자기 이름 반환


if __name__ == "__main__":
    the_host = Moviemon(12345, "괴물", "some.image.url", "4.5")
    print(the_host)
