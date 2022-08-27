pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
        google()
    }
}

rootProject.name = "OrderBroker"

include(":android")
include(":desktop")
include(":common")
include(":shared")
