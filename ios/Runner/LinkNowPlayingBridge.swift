import Flutter

/// The remote Now Playing extension requires iOS 27 and an App Group.
final class LinkNowPlayingBridge {
    private let channel: FlutterMethodChannel

    init(messenger: FlutterBinaryMessenger) {
        channel = FlutterMethodChannel(name: "com.zarz.mornye/link_now_playing", binaryMessenger: messenger)
        channel.setMethodCallHandler { call, result in
            result(call.method == "supported" ? false : nil)
        }
    }

    deinit { channel.setMethodCallHandler(nil) }
}
