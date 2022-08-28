buildscript {
    extra["kotlin_version"] = "1.7.10"
    extra["ktor_version"] = "2.0.3"
    extra["junit_version"] = "5.9.0"
    extra["compose_ext_version"] = "1.3.0-beta01"
    extra["moko_res_version"] = "0.20.1"
    extra["android_target_sdk_version"] = 33
    extra["android_min_sdk_version"] = 24
    extra["android_build_tool_version"] = "33.0.0"

    extra["organization"] = "io.github.untactorder"
    extra["version"] = "1.0.0"

    repositories {
        gradlePluginPortal()
        mavenCentral()
        google()
    }

    dependencies {
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:${project.extra["kotlin_version"]}")
        classpath("org.jetbrains.kotlin:kotlin-serialization:${project.extra["kotlin_version"]}")
        classpath("com.android.tools.build:gradle:7.2.2")
    }
}

plugins {
    /**
     * Compose Gradle Plugin
     * https://plugins.gradle.org/plugin/org.jetbrains.compose
     */
    id("org.jetbrains.compose").version("1.2.0-alpha01-dev770").apply(true)
    /**
     * Moko Resources
     * https://github.com/icerockdev/moko-resources
     */
    id("dev.icerock.mobile.multiplatform-resources").version("0.20.1").apply(true)
}

allprojects {
    repositories {
        mavenCentral()
        mavenLocal()
        google()

        maven {
            setUrl("https://jitpack.io")
            setUrl("https://kotlin.bintray.com/kotlinx")
            setUrl("https://maven.pkg.jetbrains.space/public/p/compose/dev")
        }
    }
}

tasks.register("clean", Delete::class) {
    delete(rootProject.buildDir)
}
