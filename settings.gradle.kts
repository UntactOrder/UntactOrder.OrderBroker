pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
        google()
        maven {
            setUrl("https://jitpack.io")
            setUrl("https://kotlin.bintray.com/kotlinx")
            setUrl("https://maven.pkg.jetbrains.space/public/p/compose/dev")
        }
    }

    plugins {
        //kotlin("jvm").version(rootProject.extra["kotlin_version"] as String)
        id("org.jetbrains.compose").version("1.3.0-alpha02")
    }
}

rootProject.name = "OrderBroker"
include(":androidApp")
//include(":shared")
include(":layout")
