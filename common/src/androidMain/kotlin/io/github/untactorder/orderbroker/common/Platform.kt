package io.github.untactorder.orderbroker.common

actual fun getPlatformName(): String {
    return "Android ${android.os.Build.VERSION.SDK_INT}"
}
