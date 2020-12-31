from dataclasses import dataclass, field

from cryptobox._cbox import lib, ffi


@dataclass
class PreKey:
    id: int = field()
    data: bytes = field()


class CBox:
    def __init__(self):
        self._ptr_ptr = ffi.new("struct CBox * *")
        self._init = False

    def file_open(self, path: str):
        r = lib.cbox_file_open(path.encode("utf8"), self._ptr_ptr)
        self._init = True
        print(r)

    @property
    def _ptr(self):
        if self._init:
            return self._ptr_ptr[0]
        else:
            raise Exception("CBox not initialized")

    def decrypt(self, from_: str, sender: str, text: bytes):
        sid = generate_session_id(from_, sender)
        session = self.session_from_message(sid, text)
        return session.get_message()

    def close(self):
        r = lib.cbox_close(self._ptr)

    def new_pre_key(self, pre_key_id: int) -> PreKey:
        vec = CBoxVec()
        r = lib.cbox_new_prekey(self._ptr, pre_key_id, vec._ptr_ptr)
        return PreKey(id=pre_key_id, data=vec.bytes())

    def new_last_pre_key(self) -> PreKey:
        return self.new_pre_key(lib.CBOX_LAST_PREKEY_ID)

    def session_from_prekey(self, session_id: str, prekey: bytes):
        session = CBoxSession(self)
        size = ffi.new("size_t *")
        size_p = len(prekey)
        r = lib.cbox_session_init_from_prekey(
            self._ptr,
            ffi.new("unsigned char *", 1),
            # ffi.new("unsigned char *"),
            prekey.encode("utf8"),
            # size[0],
            size_p,
            session._ptr_ptr
        )
        session._init = True

    def session_from_message(self, session_id: str, cipher: bytes):
        session = CBoxSession(self)
        vec = CBoxVec()
        size = ffi.new("size_t *")
        size_p = len(cipher)
        r = lib.cbox_session_init_from_message(
            self._ptr,
            session_id.encode("utf8"),
            cipher,
            size_p,
            session._ptr_ptr,
            vec._ptr_ptr
        )
        session._init = True
        session._message = vec.bytes()
        return session


def generate_session_id(user_id: str, client_id):
    return f"{user_id}_{client_id}"


class CBoxVec:
    def __init__(self):
        self._ptr_ptr = ffi.new("struct CBoxVec * *")

    @property
    def _ptr(self):
        return self._ptr_ptr[0]

    def len(self):
        return lib.cbox_vec_len(self._ptr)

    def bytes(self) -> bytes:
        arr = ffi.unpack(lib.cbox_vec_data(self._ptr), self.len())
        return bytes(arr)


class CBoxSession:
    def __init__(self, cbox: CBox):
        self._ptr_ptr = ffi.new("struct CBoxSession * *")
        self._init = False
        self.cbox = cbox
        self._message: bytes = b''

    @property
    def _ptr(self):
        if self._init:
            return self._ptr_ptr[0]
        else:
            raise Exception("CBox not initialized")

    def get_message(self):
        return self._message

    def decrypt(self, cipher: bytes) -> bytes:
        vec = CBoxVec()
        r = lib.cbox_decrypt(
            self._ptr,
            cipher,
            len(cipher),
            vec._ptr_ptr
        )
        return vec.bytes()

