class TeXfile:
    def __init__(self, filename, terms, friendlyName):
        self.filename = filename
        self.friendlyName = friendlyName
        self.replaceTerms = terms

frTermsOEQ = {
        "\*title": "Title:",
        "\*pages": "Pages:",
        "\*OEa": "Event 1:",
        "\*OEb": "Event 2:",
        "\*OEc": "Event 3:",
        "\*OEd": "Event 4:",
        "\*OEe": "Event 5:",
        "\*OEf": "Event 6:",
        "\*OEg": "Event 7:",
        "\*OEh": "Event 8:",
        "\*OEi": "Event 9:",
        "\*OEj": "Event 10",
        "\*Qa": "Question 1:",
        "\*Qb": "Question 2:",
        "\*Qc": "Question 3:"
}

frTermsWOutline = {
        "\*q1" : "Question 1:",
        "\*q2" : "Question 2:",
        "\*q3" : "Question 3:"
}


OEQuiz = TeXfile("oequiz.tex.bk", frTermsOEQ, "Reading Quiz, Ordinal + Questions")
WOutline = TeXfile("writingoutline.tex.bk", frTermsWOutline, "Writing Outline")

Qformats = [OEQuiz, WOutline]
