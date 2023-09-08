import streamlit as st

# def display_box(title, value):
#     box = f"""
#     <div style="padding:20px; border: 2px solid black; border-radius: 5px; margin: 5px">
#         <h3 style="color:blue;">{title}</h3>
#         <p style="font-size:19px;">{value}</p>
#     </div>
#     """
#     st.markdown(box, unsafe_allow_html=True)


# def display_box(title, value, query):
#     if st.button(title):  # 버튼을 사용하여 박스를 구현
#         st.text(query)  # 버튼 클릭 시 쿼리문을 출력

def display_box(title, value, query):
    box = f"""
    <div style="padding:20px; border: 2px solid black; border-radius: 5px; margin: 5px">
        <h3 style="color:blue;">{title}</h3>
        <p style="font-size:19px;">{value}</p>
        <div style="margin-top:10px; background-color: #f0f0f0; padding: 5px; border: 1px dashed #888; border-radius: 3px;">
            <span style="font-size:16px; font-family: monospace;">{query}</span>
        </div>
    </div>
    """
    st.markdown(box, unsafe_allow_html=True)

def wrap_text_by_char_count(text, char_limit):
    words = text.split()
    lines, current_line = [], words[0]

    for word in words[1:]:
        if len(current_line) + len(word) + 1 > char_limit:
            lines.append(current_line)
            current_line = word
        else:
            current_line += ' ' + word

    lines.append(current_line)
    return '\n'.join(lines)