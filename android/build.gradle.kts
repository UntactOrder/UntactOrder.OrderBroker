plugins {
    id("org.jetbrains.compose")
    id("com.android.application")
    kotlin("android")
}

group = "io.github.untactorder"
version = "1.0"

android {
    namespace = "io.github.untactorder.ui"
    compileSdk = rootProject.extra["android_target_sdk_version"] as Int?
    buildToolsVersion = rootProject.extra["android_build_tool_version"] as String
    testOptions {
        unitTests.apply {
            isReturnDefaultValues = true
        }
    }
    defaultConfig {
        applicationId = "io.github.untactorder.ui"
        minSdk = rootProject.extra["android_min_sdk_version"] as Int?
        targetSdk = rootProject.extra["android_target_sdk_version"] as Int?
        versionCode = 1
        versionName = "1.0.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables.useSupportLibrary = true
    }
    buildTypes {
        getByName("release") {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility(JavaVersion.VERSION_1_8)
        targetCompatibility(JavaVersion.VERSION_1_8)
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.3.0-beta01"
    }
    packagingOptions {
        resources.excludes += "/META-INF/{AL2.0,LGPL2.1}"
    }
}

dependencies {
    implementation(project(":layout"))
    //implementation(project(":shared"))
}