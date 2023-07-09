Ein Programm dass das Formulieren von englischsprachigem Text vereinfachen soll. Hierzu werden verschiedene Ansätze des Natural Language Processing angewendet. 

Die Anwendung lädt sich bei Bedarf entsprechende Modelle aus dem Internet, diese dienen jedoch tendenziell eher Demozwecken (da es sich hierbei um recht leichtgewichtige Modelle handelt). Um bei Bedarf die Ergebnisse zu verbessern, können eigene Modelle verwendet werden. 

Funktionen:
- Translation (default model: Helsinki-NLP/opus-mt-de-en)
- Text-Generation: kann einzelne Wörter oder ganze Abschnitte generieren (default model: gpt2-small)
- Synonyms: mithilfe eines Word2Vec models werden die Kontextuell nahestehendsten Wörter vorgeschlagen (Default model: glove-wiki-gigaword-50)
- Spell Check: nutzt language-tool um Fehler zu finden und zu markieren
