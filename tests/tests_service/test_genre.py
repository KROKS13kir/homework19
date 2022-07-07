from unittest.mock import MagicMock

import pytest as pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService
from setup_db import db


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    comedy = Genre(id=1, name='Комедия')
    family = Genre(id=2, name='Семейный')
    fantasy = Genre(id=3, name='Фэнтези')

    genre_dao.get_one = MagicMock(return_value=comedy)
    genre_dao.get_all = MagicMock(return_value=[comedy, family, fantasy])
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()
    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def user_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre != None
        assert genre.id != None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        genre_new = {
            "name": "Экшн",
        }
        genre = self.genre_service.create(genre_new)
        assert genre.id != None

    def test_delete(self):
        self.genre_service.delete(1)

    def test_update(self):
        genre_up = {
            "id": 2,
            "name": "Хоррор",
        }
        self.genre_service.update(genre_up)