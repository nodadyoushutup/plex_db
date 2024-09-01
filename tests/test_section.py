from app.section import Section

def test_create_section(test_app):
    section = Section.create(
        agent="tv.plex.agents.movie",
        allow_sync=True,
        art="/:/resources/movie-fanart.jpg",
        composite="/library/sections/1/composite/1725124245",
        filters=True,
        key=1,
        language="en-US",
        locations="/media/movies/mainstream",
        refreshing=False,
        scanner="Plex Movie",
        thumb="/:/resources/movie.png",
        title="Mainstream",
        type="movie",
        uuid="057c1508-8981-41fb-a025-b4b4e870aacf"
    )
    assert section.agent == "tv.plex.agents.movie"
    assert section.allow_sync is True
    assert section.art == "/:/resources/movie-fanart.jpg"
    assert section.composite == "/library/sections/1/composite/1725124245"
    assert section.filters is True
    assert section.key == 1
    assert section.language == "en-US"
    assert section.locations == "/media/movies/mainstream"
    assert section.refreshing is False
    assert section.scanner == "Plex Movie"
    assert section.thumb == "/:/resources/movie.png"
    assert section.title == "Mainstream"
    assert section.type == "movie"
    assert section.uuid == "057c1508-8981-41fb-a025-b4b4e870aacf"

def test_get_by_id(test_app):
    section = Section.create(
        agent="tv.plex.agents.movie",
        allow_sync=True,
        title="Mainstream",
        uuid="057c1508-8981-41fb-a025-b4b4e870aacf"
    )
    retrieved = Section.get_by_id(section.id)
    assert retrieved.id == section.id

def test_get_by_uuid(test_app):
    section = Section.create(
        agent="tv.plex.agents.movie",
        allow_sync=True,
        title="Mainstream",
        uuid="057c1508-8981-41fb-a025-b4b4e870aacf"
    )
    retrieved = Section.get_by_id("057c1508-8981-41fb-a025-b4b4e870aacf")
    assert retrieved.uuid == "057c1508-8981-41fb-a025-b4b4e870aacf"

def test_update_section(test_app):
    section = Section.create(
        agent="tv.plex.agents.movie",
        allow_sync=True,
        title="Mainstream",
        uuid="057c1508-8981-41fb-a025-b4b4e870aacf"
    )
    section.update(title="Updated Title")
    assert section.title == "Updated Title"

def test_delete_section(test_app):
    section = Section.create(
        agent="tv.plex.agents.movie",
        allow_sync=True,
        title="Mainstream",
        uuid="057c1508-8981-41fb-a025-b4b4e870aacf"
    )
    section.delete()
    assert Section.get_by_id(section.id) is None

def test_get_all_sections(test_app):
    Section.create(
        agent="tv.plex.agents.movie",
        allow_sync=True,
        title="Mainstream",
        uuid="057c1508-8981-41fb-a025-b4b4e870aacf"
    )
    Section.create(
        agent="tv.plex.agents.movie",
        allow_sync=True,
        title="Second Section",
        uuid="abc12345-6789-41fb-a025-b4b4e870aaaa"
    )
    sections = Section.get()
    assert len(sections) >= 2
