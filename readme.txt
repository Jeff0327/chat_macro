<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE readme [
<!ELEMENT readme (title, introduction, usage, notes, support)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT introduction (#PCDATA)>
<!ELEMENT usage (step*)>
<!ELEMENT step (title, description)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT notes (note*)>
<!ELEMENT note (type, content)>
<!ELEMENT type (#PCDATA)>
<!ELEMENT content (#PCDATA)>
<!ELEMENT support (contact*)>
<!ELEMENT contact (#PCDATA)>
]>

<readme>
  <title>채팅 매크로</title>
  <introduction>간편한 채팅 매크로 도구로, 반복적인 채팅 입력을 자동화합니다.</introduction>

  <usage>
    <step>
      <title>1. main.exe 다운로드</title>
      <description>GitHub 저장소에서 <code>main.exe</code> 파일을 다운로드합니다.</description>
    </step>
    <step>
      <title>2. 채팅에 입력할 내용 복사</title>
      <description>입력할 채팅 내용을 복사합니다. (Ctrl+C)</description>
    </step>
    <step>
      <title>3. 실행 간격 설정</title>
      <description>실행 파일을 실행하고, 채팅 입력 간격을 초 단위로 설정합니다.</description>
    </step>
    <step>
      <title>4. 프로그램 이동 후 시작</title>
      <description>매크로 시작 후, 자동 입력을 원하는 프로그램으로 이동합니다.</description>
    </step>
  </usage>

  <notes>
    <note>
      <type>바이러스 경고</type>
      <content>일부 바이러스 감지 프로그램이 <code>main.exe</code> 파일을 잘못 감지할 수 있습니다. 파일이 안전한지 확인하고, 필요한 경우 예외 설정을 하십시오.</content>
    </note>
    <note>
      <type>책임 한계</type>
      <content>이 도구로 인한 문제는 사용자에게 책임이 있습니다. 적절히 사용해 주세요.</content>
    </note>
  </notes>

  <support>
    <contact>문제가 발생하면 <a href="https://github.com/chat_macro/issues">GitHub Issues</a>에 보고해 주세요.</contact>
    <contact>추가적인 도움이나 피드백은 커뮤니티 포럼을 통해 제공됩니다.</contact>
  </support>
</readme>
