import Flutter
import Foundation
import UIKit

@MainActor
final class PlayerWidgetBridge {
    static let shared = PlayerWidgetBridge()
    private var channel: FlutterMethodChannel?
    private var ready = false
    private var pending: [(UUID, String, CheckedContinuation<Bool, Never>)] = []

    func attach(_ messenger: FlutterBinaryMessenger) {
        let channel = FlutterMethodChannel(name: "com.zarz.mornye/player_widget", binaryMessenger: messenger)
        self.channel = channel
        // This sideload build has no widget extension or App Group entitlement.
        channel.setMethodCallHandler { call, result in
            switch call.method {
            case "getInstalledWidgetCount": result(0)
            case "ready":
                self.ready = true
                self.flush()
                result(nil)
            case "update": result(nil)
            default: result(FlutterMethodNotImplemented)
            }
        }
    }

    func perform(_ command: String) async -> Bool {
        guard ["play", "pause", "toggle", "previous", "next", "open"].contains(command) else { return false }
        return await withCheckedContinuation { continuation in
            let id = UUID()
            pending.append((id, command, continuation))
            flush()
            Task { [weak self] in
                try? await Task.sleep(nanoseconds: 15_000_000_000)
                self?.finish(id, success: false)
            }
        }
    }

    private var sent = Set<UUID>()

    private func flush() {
        guard ready, let channel else { return }
        for (id, command, _) in pending where !sent.contains(id) {
            sent.insert(id)
            channel.invokeMethod("command", arguments: command) { [weak self] result in
                self?.finish(id, success: result as? Bool == true)
            }
        }
    }

    private func finish(_ id: UUID, success: Bool) {
        guard let index = pending.firstIndex(where: { $0.0 == id }) else { return }
        let entry = pending.remove(at: index)
        sent.remove(id)
        entry.2.resume(returning: success)
    }

}
