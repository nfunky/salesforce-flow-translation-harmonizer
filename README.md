# salesforce-flow-translation-harmonizer
A small python script that harmonizes heterogeneous Salesforce flow translations to the latest flow version using bilingual stf file(s) as input. Can be used to overcome Salesforce flow translation limitations.

Move from a bilingual stf file exported from Salesforce with diffferent flow versions to a new file containing only the latest flow translations with harmonized flow versions.

## Example input file:
```
Language code: de
Type: Bilingual

------------------TRANSLATED-------------------
Flow.Flow.AutomateCases.1.Name	Case Automation	Automatisierung Kundenvorgang	-
Flow.Flow.AutomateCases.10.Name	Case Automation	Automatisierung Kundenvorgang	-
Flow.Flow.AutomateCases.11.Name	Case Automation	Automatisierung Kundenvorgang	-
Flow.Flow.AutomateCases.9.Name	Case Automation	Automatisierung Kundenvorgang	-
Flow.Flow.AccountStatusAutomation.1.Name	Account Status Automation	Automatisierung Account Zustand	-
Flow.Flow.AccountStatusAutomation.16.Name	Account Status Automation	Automatisierung Account Zustand	-
Flow.Flow.AccountStatusAutomation.17.Name	Account Status Automation	Automatisierung Account Zustand	-
Flow.Flow.AccountStatusAutomation.18.Name	Account Status Automation	Automatisierung Account Zustand	-
Flow.Flow.AccountStatusAutomation.19.Name	Account Status Automation	Automatisierung Account Zustand	-
Flow.Flow.AccountStatusAutomation.2.Name	Account Status Automation	Automatisierung Account Zustand	-
Flow.Flow.AccountStatusAutomation.12.Choice.Identify.FieldLabel	Identify	Identifizierung	-
Flow.Flow.AccountStatusAutomation.11.Choice.Propose.FieldLabel	Propose	Angebot	-
Flow.Flow.AccountStatusAutomation.10.Choice.Close.FieldLabel	Close	Schließen	-
Flow.Flow.AccountStatusAutomation.5.Choice.Cancel.FieldLabel	Cancel	Abbruch	-
Flow.Flow.AutomateCases.10.Choice.NewBusiness.FieldLabel	New Business	Neues Geschäft	-
Flow.Flow.AutomateCases.10.Choice.ExistingBusiness.FieldLabel	Existing Business	Bestehendes Geschäft	-
Flow.Flow.AutomateCases.9.Choice.ExistingBusiness.FieldLabel	Business	Geschäft	-
Flow.Flow.AutomateCases.9.Choice.RampUpBusiness.FieldLabel	Ramp Up	Zusatzgeschäft	-
Flow.Flow.AutomateCases.4.Choice.RampUpBusiness.FieldLabel	Ramp Up	Geschäft	-
```
## Example output file:
```
Language code: de
Type: Bilingual

------------------TRANSLATED-------------------
Flow.Flow.AutomateCases.11.Name	Case Automation	Automatisierung Kundenvorgang	-
Flow.Flow.AutomateCases.11.Choice.NewBusiness.FieldLabel	New Business	Neues Geschäft	-
Flow.Flow.AutomateCases.11.Choice.ExistingBusiness.FieldLabel	Business	Geschäft	-
Flow.Flow.AutomateCases.11.Choice.RampUpBusiness.FieldLabel	Ramp Up	Geschäft	-
Flow.Flow.AccountStatusAutomation.19.Name	Account Status Automation	Automatisierung Account Zustand	-
Flow.Flow.AccountStatusAutomation.19.Choice.Identify.FieldLabel	Identify	Identifizierung	-
Flow.Flow.AccountStatusAutomation.19.Choice.Propose.FieldLabel	Propose	Angebot	-
Flow.Flow.AccountStatusAutomation.19.Choice.Close.FieldLabel	Close	Schließen	-
Flow.Flow.AccountStatusAutomation.19.Choice.Cancel.FieldLabel	Cancel	Abbruch	-
```

# Usage
The script is able to harmonize single files as well as entire directories containing a collection of stf files.
To harmonize a single stf file use the following command:
>harmonize-flow-translations.py -f [FILENAME]

To harmonize a collection of stf files within a directory use the following command:
>harmonize-flow-translations.py -d [DIRECTORY]


