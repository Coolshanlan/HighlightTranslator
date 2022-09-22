import deepl
import GoogleTranslate as gt

def get_translate(inputtext,**kwargs):
    try:
        return gt.get_translate(deepl.translate(source_language="EN", target_language="ZH", text=inputtext),'zh-CN','zh-TW')
    except Exception:
        return None

if __name__ == "__main__":
    print(get_translate(inputtext='''data_transform: This is the one responsible to modify the dataset, and transform the data to do it usable for the model.

Null values: By the moment only replace with the most used value in the column.
Non numeric values: At this moment stops the treatment. In this versión the function only accepts numeric columns.
Normalize Data.: It's possible to indicate a maximum standard desviation, and the function normalize the columns with a std bigger than the one indicated
'''))
