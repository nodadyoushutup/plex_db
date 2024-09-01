from app.library import Library


def test_create(test_app):
    library = Library.create(identifier="test_id", mediaTagVersion="v1", title1="Title1", title2="Title2")
    assert library.identifier == "test_id"
    assert library.mediaTagVersion == "v1"
    assert library.title1 == "Title1"
    assert library.title2 == "Title2"

def test_get_by_id(test_app):
    library = Library.create(identifier="test_id_2", mediaTagVersion="v2", title1="Title1", title2="Title2")
    retrieved = Library.get_by_id(library.id)
    assert retrieved.id == library.id

def test_update(test_app):
    library = Library.create(identifier="test_id_3", mediaTagVersion="v3", title1="Title1", title2="Title2")
    library.update(title1="Updated Title")
    assert library.title1 == "Updated Title"

def test_delete(test_app):
    library = Library.create(identifier="test_id_4", mediaTagVersion="v4", title1="Title1", title2="Title2")
    library.delete()
    assert Library.get_by_id(library.id) is None

def test_get(test_app):
    Library.create(identifier="test_id_5", mediaTagVersion="v5", title1="Title1", title2="Title2")
    Library.create(identifier="test_id_6", mediaTagVersion="v6", title1="Title1", title2="Title2")
    libraries = Library.get()
    assert len(libraries) >= 2
