# DDE-Lite
Mini version of DDE tool.  Executed from python environment, instead of C# .NET.  The original version is available at https://github.com/ananddotiyer/DDE.  

DDE-Lite (Data Drive Engine) is a set of python scripts that helps extend typical Excel functionalities, like its formulae and macros.  On top of that, the tool allows to create massive amounts of data that follows a specified template, characterized by a set of rules.  This will greatly enhance the effectiveness of testing, specifically automated and performance testing.

At the heart of the program is the concept of a data template, that, simply put, is a textual representation of an excel sheet.  In the present version of DDE (DDE-Lite), you must manually populate the template with custom rules, which in turn can be used to create huge amounts of customized data, to easily fill up the web page during a performance test run.

The rules could vary in complexity and can handle simple data validation (as seen in Excel) rules, to very complicated user-defined functions (as defined from Python).  It also supports the cross-references between excel cells, INDIRECT references (as supported in Excel), and has built-in concatenation methods, both of which are available out-of-the-box. 

For more insights into workflow, usage instructions, and prerequisites of the tool, see <a href='https://github.com/ananddotiyer/DDE-Lite/blob/master/Help/readme.pdf'>Help documentation</a>
