package io.github.untactorder.orderbroker.common

import platform.UIKit.UIDevice

actual fun getPlatformName(): String {
    return UIDevice.currentDevice.systemName() + " " + UIDevice.currentDevice.systemVersion
}
