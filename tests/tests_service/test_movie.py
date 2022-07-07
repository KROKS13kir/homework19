from unittest.mock import MagicMock

import pytest as pytest

from dao.movie import MovieDAO
from dao.model.movie import Movie
from dao.model.genre import Genre
from dao.model.director import Director

from service.movie import MovieService
from setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    firstMovie = Movie(id=1, title='Йеллоустоун',
                       description='Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»',
                       trailer='https://www.youtube.com/watch?v=UKei_d0cbP4', year=2018, rating=8.6, genre_id=17,
                       director_id=1)
    secondMovie = Movie(id=2, title='Омерзительная восьмерка',
                        description='США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество: генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.',
                        trailer='https://www.youtube.com/watch?v=lmB9VWm0okU', year=2015, rating=7.8, genre_id=4,
                        director_id=2)

    movie_dao.get_one = MagicMock(return_value=firstMovie)
    movie_dao.get_all = MagicMock(return_value=[firstMovie, secondMovie])
    movie_dao.create = MagicMock(return_value=Movie(id=2))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie != None
        assert movie.id != None

    def test_get_all(self):
        movies = self.movie_service.get_all(filters={})
        assert len(movies) > 0

    def test_create(self):
        movie_new = {
            "title": "Гарри Поттер мой кумир!",
            "trailer": "таким фильмам не нужны трейлеры",
            "year": 1990,
            "rating": 10,
            "description": "10 из 10!"
        }
        movie = self.movie_service.create(movie_new)
        assert movie.id != None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_up = {
            "id": 21,
            "title": "-------",
            "trailer": "-----",
            "year": 0,
            "rating": 0,
            "description": "0 из 10!",
            "genre_id": 1,
            "director_id": 1
        }
        self.movie_service.update(movie_up)
