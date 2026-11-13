Name:		dependency-analysis-gradle-plugin
Version:	3.4.0
Release:	1
Summary:	Gradle plugin that reports unused and misused dependencies
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/autonomousapps/dependency-analysis-android-gradle-plugin
# Tag v3.4.0 (95ce05b90291688806efd91fb1af045642e9c6ce).
# The upstream build is Gradle. This package compiles the plugin with kotlinc.
# kotlin-editor 0.18 core and gradle-script-grammar 0.5 are vendored as source.
# com.android.Version is the AOSP class, loaded from android-gradle-api 9.0.0
# version.properties. com.android.tools.build:gradle is not packaged.
Source0:	dependency-analysis-gradle-plugin-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-21-openjdk-devel
BuildRequires:	kotlin = 2.0.21
BuildRequires:	kotlin-libs = 2.0.21
BuildRequires:	antlr4-tool
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	gradle
BuildRequires:	mvn(com.squareup.moshi:moshi) = 1.15.2
BuildRequires:	mvn(com.squareup.moshi:moshi-adapters) = 1.15.2
BuildRequires:	mvn(com.squareup.moshi:moshi-kotlin) = 1.15.2
BuildRequires:	mvn(dev.zacsweers.moshix:moshi-sealed-runtime) = 0.30.0
BuildRequires:	mvn(dev.zacsweers.moshix:moshi-sealed-reflect) = 0.30.0
BuildRequires:	mvn(com.squareup.okio:okio)
BuildRequires:	mvn(com.google.code.findbugs:jsr305)
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-metadata-jvm) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-tooling-core) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-gradle-plugin) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-gradle-plugin-api) = 2.4.21
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(com.github.ben-manes.caffeine:caffeine)
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	mvn(org.antlr:antlr4-runtime)
BuildRequires:	mvn(org.ow2.asm:asm) = 9.11.1
BuildRequires:	mvn(org.ow2.asm:asm-tree) = 9.11.1
BuildRequires:	mvn(org.jetbrains:annotations)
BuildRequires:	mvn(com.android.tools:annotations) = 32.0.0
BuildRequires:	mvn(com.android.tools.build:builder-model) = 9.0.0
BuildRequires:	mvn(com.android.tools.build:gradle-api) = 9.0.0

%description
Dependency Analysis Gradle plugin %{version}.
DependencyAnalysisPlugin reports dependencies a JVM project declares but
does not use. BuildHealthPlugin reports the same thing across a build.

%prep
%autosetup -n dependency-analysis-gradle-plugin-%{version}
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s LICENSE.txt
test -s upstream/src/main/kotlin/com/autonomousapps/DependencyAnalysisPlugin.kt
test -s upstream/graph-support/src/main/kotlin/com/autonomousapps/graph/Graphs.kt
test -s upstream/variant-artifacts/src/main/kotlin/com/autonomousapps/artifacts/VariantArtifacts.kt
test -s vendor/kotlin-editor/cash/grammar/kotlindsl/parse/Parser.kt
test -s grammar/simple/Simple.g4
test -s grammar/kotlin/KotlinParser.g4
test -s grammar/kotlin/UnicodeClasses.g4
test -s grammar/gradle/GradleScriptLexer.g4
test -s agp/Version.java
grep -F -qx 'buildVersion=9.0.0' agp/version.properties
test -s overlay/BuildConfig.kt
grep -F -q 'GRADLE_MIN_VERSION: String = "8.11.1"' overlay/BuildConfig.kt
grep -F -q 'GRADLE_MAX_VERSION: String = "9.1.0"' overlay/BuildConfig.kt
test -s overlay/projects.kt
test -s check/DagpCheck.java
test -s build.sh
test -s check.sh

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./build.sh
test -s dependency-analysis-gradle-plugin.jar

cat > dependency-analysis-gradle-plugin.pom << END
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.autonomousapps</groupId>
  <artifactId>dependency-analysis-gradle-plugin</artifactId>
  <version>%{version}</version>
  <name>Dependency Analysis Gradle Plugin</name>
  <description>Analyzes dependency usage in Android and JVM projects.</description>
  <url>https://github.com/autonomousapps/dependency-analysis-android-gradle-plugin</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>javax.inject</groupId>
      <artifactId>javax.inject</artifactId>
      <version>1.0.5</version>
    </dependency>
    <dependency>
      <groupId>com.squareup.moshi</groupId>
      <artifactId>moshi</artifactId>
      <version>1.15.2</version>
    </dependency>
    <dependency>
      <groupId>com.squareup.moshi</groupId>
      <artifactId>moshi-adapters</artifactId>
      <version>1.15.2</version>
    </dependency>
    <dependency>
      <groupId>com.squareup.moshi</groupId>
      <artifactId>moshi-kotlin</artifactId>
      <version>1.15.2</version>
    </dependency>
    <dependency>
      <groupId>dev.zacsweers.moshix</groupId>
      <artifactId>moshi-sealed-runtime</artifactId>
      <version>0.30.0</version>
    </dependency>
    <dependency>
      <groupId>dev.zacsweers.moshix</groupId>
      <artifactId>moshi-sealed-reflect</artifactId>
      <version>0.30.0</version>
    </dependency>
    <dependency>
      <groupId>com.squareup.okio</groupId>
      <artifactId>okio</artifactId>
      <version>3.6.0</version>
    </dependency>
    <dependency>
      <groupId>com.google.code.findbugs</groupId>
      <artifactId>jsr305</artifactId>
      <version>3.0.2</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>33.6.0-jre</version>
    </dependency>
    <dependency>
      <groupId>com.github.ben-manes.caffeine</groupId>
      <artifactId>caffeine</artifactId>
      <version>3.0.5</version>
    </dependency>
    <dependency>
      <groupId>org.antlr</groupId>
      <artifactId>antlr4-runtime</artifactId>
      <version>4.13.2</version>
    </dependency>
    <dependency>
      <groupId>org.ow2.asm</groupId>
      <artifactId>asm</artifactId>
      <version>9.11.1</version>
    </dependency>
    <dependency>
      <groupId>org.ow2.asm</groupId>
      <artifactId>asm-tree</artifactId>
      <version>9.11.1</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-stdlib</artifactId>
      <version>2.0.21</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-reflect</artifactId>
      <version>2.0.21</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-metadata-jvm</artifactId>
      <version>2.4.21</version>
    </dependency>
  </dependencies>
</project>
END

%install
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
mkdir -p %{buildroot}
sysjar install --buildroot %{buildroot} \
	--artifact dependency-analysis-gradle-plugin.pom:dependency-analysis-gradle-plugin.jar \
	--file-name dependency-analysis-gradle-plugin \
	--filelist installed.files
grep -F -q '%%dir /usr/share/sysjar/index/com.autonomousapps' installed.files
test -s %{buildroot}%{_javadir}/dependency-analysis-gradle-plugin.jar

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./check.sh %{buildroot}%{_javadir}/dependency-analysis-gradle-plugin.jar

%files -f installed.files
