package io.github.untactorder.orderbroker

actual fun getPlatformName(): String {
    return "Android ${android.os.Build.VERSION.SDK_INT}"
}
