import string
from datetime import date

from tsidpy import TSID


class UrlService:
    BASE62_ALPHABET: str = (
        string.digits + string.ascii_lowercase + string.ascii_uppercase
    )

    def is_expired(self, expiration_date: date | None) -> bool:
        """
        url의 expiration_date 가 지났는지 확인

        Returns:
        - bool: 만료 True, 그렇지 않으면 False
        """

        if expiration_date is None:
            return False

        return date.today() > expiration_date

    def encode_by_base62(self, url_tsid: int) -> str:
        """
        숫자를 Base-62 문자열로 변환
        """
        if url_tsid == 0:
            return self.BASE62_ALPHABET[0]

        base62 = []

        while url_tsid:
            url_tsid, rem = divmod(url_tsid, 62)
            base62.append(self.BASE62_ALPHABET[rem])

        return "".join(reversed(base62))

    def decode_by_base62(self, short_key: str) -> int:
        """
        Base62로 인코딩된 문자열을 받아서 TSID로 디코딩하는 함수
        """
        url_tsid = 0

        for char in short_key:
            url_tsid = url_tsid * 62 + self.BASE62_ALPHABET.index(char)

        return url_tsid

    @staticmethod
    def tsid_generator() -> int:
        tsid: TSID = TSID.create().number
        return tsid
