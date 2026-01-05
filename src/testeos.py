a = {"hi":{"croquis":"im croquis","figura":"this figura","button":"this button"}}
a.update({"HI":{"croquis":"IM CROQUIS","figura":"THIS FIGURA","button":"THIS BUTTON"}})
for i in list(a.values()):
    print(i["figura"])