from .library import Library
from .config import app, db
from .model import Model


class Server(Model):
    baseurl = db.Column(db.String)
    token = db.Column(db.String)
    timeout = db.Column(db.Integer)


    allowCameraUpload = db.Column(db.Boolean)
    allowChannelAccess = db.Column(db.Boolean)
    allowMediaDeletion = db.Column(db.Boolean)
    allowSharing = db.Column(db.Boolean)
    allowSync = db.Column(db.Boolean)
    backgroundProcessing = db.Column(db.Boolean)
    certificate = db.Column(db.Boolean)
    companionProxy = db.Column(db.Boolean)
    # diagnostics = db.Column(db.String)  # Relationship (future, don't touch)
    eventStream = db.Column(db.Boolean)
    friendlyName = db.Column(db.String)
    hubSearch = db.Column(db.Boolean)
    machineIdentifier = db.Column(db.String)
    multiuser = db.Column(db.Boolean)
    myPlex = db.Column(db.Boolean)
    myPlexMappingState = db.Column(db.String)
    myPlexSigninState = db.Column(db.String)
    myPlexSubscription = db.Column(db.Boolean)
    myPlexUsername = db.Column(db.String)
    # ownerFeatures = db.Column(db.String)  # Relationship (future, don't touch)
    photoAutoTag = db.Column(db.String)
    platform = db.Column(db.String)
    platformVersion = db.Column(db.String)
    pluginHost = db.Column(db.Boolean)
    readOnlyLibraries = db.Column(db.Integer)
    requestParametersInCookie = db.Column(db.String)
    streamingBrainVersion = db.Column(db.String)
    sync = db.Column(db.Boolean)
    transcoderActiveVideoSessions = db.Column(db.Integer)
    transcoderAudio = db.Column(db.Boolean)
    transcoderLyrics = db.Column(db.Boolean)
    transcoderPhoto = db.Column(db.Boolean)
    transcoderSubtitles = db.Column(db.Boolean)
    transcoderVideo = db.Column(db.Boolean)
    # transcoderVideoBitrates = db.Column(db.String)  # Relationship (future, don't touch)
    # transcoderVideoQualities = db.Column(db.String)  # Relationship (future, don't touch)
    # transcoderVideoResolutions = db.Column(db.String)  # Relationship (future, don't touch)
    updater = db.Column(db.Boolean)
    version = db.Column(db.String)
    voiceSearch = db.Column(db.Boolean)


    @classmethod
    def create(cls, obj=None, **kwargs):
        if obj is not None:
            kwargs.update({
                "baseurl": obj._baseurl,
                "token": obj._token,
                "timeout": obj._timeout
            })
            Library.create(obj.library)
        return super().create(obj=obj, **kwargs)