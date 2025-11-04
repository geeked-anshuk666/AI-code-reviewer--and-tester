import * as vscode from 'vscode';
import * as axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    console.log('AI Testing Platform extension is now active!');

    // Register commands
    let codeReview = vscode.commands.registerCommand('ai-testing-platform.codeReview', () => {
        performCodeReview();
    });

    let generateTests = vscode.commands.registerCommand('ai-testing-platform.generateTests', () => {
        generateTestsForFile();
    });

    let securityScan = vscode.commands.registerCommand('ai-testing-platform.securityScan', () => {
        performSecurityScan();
    });

    let applyFixes = vscode.commands.registerCommand('ai-testing-platform.applyFixes', () => {
        applyCodeFixes();
    });

    let runTests = vscode.commands.registerCommand('ai-testing-platform.runTests', () => {
        runGeneratedTests();
    });

    context.subscriptions.push(codeReview);
    context.subscriptions.push(generateTests);
    context.subscriptions.push(securityScan);
    context.subscriptions.push(applyFixes);
    context.subscriptions.push(runTests);

    // Register auto-review on save if enabled
    if (vscode.workspace.getConfiguration('ai-testing-platform').get('autoReview')) {
        vscode.workspace.onDidSaveTextDocument((document) => {
            if (document.languageId === 'python' || document.languageId === 'javascript' || document.languageId === 'java') {
                autoReviewDocument(document);
            }
        });
    }
}

export function deactivate() {}

async function performCodeReview() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found!');
        return;
    }

    const document = editor.document;
    const codeContent = document.getText();
    const fileName = document.fileName;
    const languageId = document.languageId;

    try {
        const config = vscode.workspace.getConfiguration('ai-testing-platform');
        const serverUrl = config.get('serverUrl', 'http://localhost:8000');
        const apiKey = config.get('apiKey', '');

        const response = await axios.default.post(`${serverUrl}/ide-integration/api/events/code_review/`, {
            code_content: codeContent,
            file_path: fileName,
            language: languageId,
            plugin_id: 1 // In a real implementation, this would be dynamically assigned
        }, {
            headers: {
                'Authorization': `Token ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        const results = response.data.results;
        
        // Display results in output panel
        const outputChannel = vscode.window.createOutputChannel('AI Code Review');
        outputChannel.clear();
        outputChannel.appendLine('AI Code Review Results:');
        outputChannel.appendLine('======================');
        
        if (results.code_analysis) {
            outputChannel.appendLine('\nCode Quality Analysis:');
            outputChannel.appendLine(`Quality Score: ${results.code_analysis.quality_score}/100`);
            outputChannel.appendLine(`Complexity: ${results.code_analysis.structure_analysis.complexity}`);
            
            if (results.code_analysis.issues && results.code_analysis.issues.length > 0) {
                outputChannel.appendLine('\nIssues Found:');
                results.code_analysis.issues.forEach((issue: any) => {
                    outputChannel.appendLine(`- ${issue.type}: ${issue.message}`);
                });
            }
        }
        
        if (results.security_analysis) {
            outputChannel.appendLine('\nSecurity Analysis:');
            outputChannel.appendLine(`Security Score: ${results.security_analysis.security_score}/100`);
            outputChannel.appendLine(`Vulnerabilities Found: ${results.security_analysis.total_issues}`);
            
            if (results.security_analysis.vulnerabilities && results.security_analysis.vulnerabilities.length > 0) {
                outputChannel.appendLine('\nSecurity Issues:');
                results.security_analysis.vulnerabilities.forEach((vuln: any) => {
                    outputChannel.appendLine(`- ${vuln.type} at line ${vuln.line}: ${vuln.code}`);
                });
            }
        }
        
        outputChannel.show(true);
        
        vscode.window.showInformationMessage('Code review completed! Check the output panel for results.');
    } catch (error) {
        vscode.window.showErrorMessage(`Error performing code review: ${error}`);
    }
}

async function generateTestsForFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found!');
        return;
    }

    const document = editor.document;
    const codeContent = document.getText();
    const fileName = document.fileName;
    const languageId = document.languageId;

    try {
        const config = vscode.workspace.getConfiguration('ai-testing-platform');
        const serverUrl = config.get('serverUrl', 'http://localhost:8000');
        const apiKey = config.get('apiKey', '');
        const testFramework = config.get('testFramework', 'pytest');

        // First, we need a project ID - in a real implementation, this would be selected by the user
        const projectId = await vscode.window.showInputBox({
            prompt: 'Enter Project ID for test generation',
            placeHolder: 'Project ID'
        });

        if (!projectId) {
            vscode.window.showErrorMessage('Project ID is required for test generation');
            return;
        }

        const response = await axios.default.post(`${serverUrl}/ide-integration/api/events/generate_tests/`, {
            code_content: codeContent,
            file_path: fileName,
            language: languageId,
            project_id: projectId,
            plugin_id: 1 // In a real implementation, this would be dynamically assigned
        }, {
            headers: {
                'Authorization': `Token ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        vscode.window.showInformationMessage(`Generated ${response.data.test_cases_generated} test cases! Check your project for the new tests.`);
    } catch (error) {
        vscode.window.showErrorMessage(`Error generating tests: ${error}`);
    }
}

async function performSecurityScan() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found!');
        return;
    }

    const document = editor.document;
    const codeContent = document.getText();
    const fileName = document.fileName;
    const languageId = document.languageId;

    try {
        const config = vscode.workspace.getConfiguration('ai-testing-platform');
        const serverUrl = config.get('serverUrl', 'http://localhost:8000');
        const apiKey = config.get('apiKey', '');

        const response = await axios.default.post(`${serverUrl}/ide-integration/api/events/security_scan/`, {
            code_content: codeContent,
            file_path: fileName,
            language: languageId,
            plugin_id: 1 // In a real implementation, this would be dynamically assigned
        }, {
            headers: {
                'Authorization': `Token ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        const results = response.data;
        
        // Display results in output panel
        const outputChannel = vscode.window.createOutputChannel('Security Scan');
        outputChannel.clear();
        outputChannel.appendLine('Security Scan Results:');
        outputChannel.appendLine('=====================');
        outputChannel.appendLine(`Security Score: ${results.security_score}/100`);
        outputChannel.appendLine(`Vulnerabilities Found: ${results.total_issues}`);
        
        if (results.vulnerabilities && results.vulnerabilities.length > 0) {
            outputChannel.appendLine('\nVulnerabilities:');
            results.vulnerabilities.forEach((vuln: any) => {
                outputChannel.appendLine(`- ${vuln.type} at line ${vuln.line}: ${vuln.code}`);
            });
        }
        
        if (results.fixes && results.fixes.length > 0) {
            outputChannel.appendLine('\nSuggested Fixes:');
            results.fixes.forEach((fix: any) => {
                outputChannel.appendLine(`- Line ${fix.line_number}: ${fix.recommendation}`);
            });
        }
        
        outputChannel.show(true);
        
        vscode.window.showInformationMessage('Security scan completed! Check the output panel for results.');
    } catch (error) {
        vscode.window.showErrorMessage(`Error performing security scan: ${error}`);
    }
}

async function applyCodeFixes() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found!');
        return;
    }

    const document = editor.document;
    const codeContent = document.getText();
    const fileName = document.fileName;
    const languageId = document.languageId;

    try {
        const config = vscode.workspace.getConfiguration('ai-testing-platform');
        const serverUrl = config.get('serverUrl', 'http://localhost:8000');
        const apiKey = config.get('apiKey', '');

        const response = await axios.default.post(`${serverUrl}/ide-integration/api/events/fix_code/`, {
            code_content: codeContent,
            file_path: fileName,
            language: languageId,
            plugin_id: 1 // In a real implementation, this would be dynamically assigned
        }, {
            headers: {
                'Authorization': `Token ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        const results = response.data;
        
        // Apply the refactored code to the editor
        const edit = new vscode.WorkspaceEdit();
        const fullRange = new vscode.Range(
            document.positionAt(0),
            document.positionAt(document.getText().length)
        );
        edit.replace(document.uri, fullRange, results.refactored_code);
        
        await vscode.workspace.applyEdit(edit);
        
        // Show a summary of applied fixes
        const outputChannel = vscode.window.createOutputChannel('Code Fixes');
        outputChannel.clear();
        outputChannel.appendLine('Code Fixes Applied:');
        outputChannel.appendLine('==================');
        outputChannel.appendLine(`Improvement: ${results.improvement_stats.improvement_percentage}%`);
        outputChannel.appendLine(`Fixes Applied: ${results.improvement_stats.fixes_applied}`);
        
        if (results.applied_fixes && results.applied_fixes.length > 0) {
            outputChannel.appendLine('\nApplied Fixes:');
            results.applied_fixes.forEach((fix: any) => {
                outputChannel.appendLine(`- ${fix.type}: ${fix.description}`);
            });
        }
        
        outputChannel.show(true);
        
        vscode.window.showInformationMessage('Code fixes applied! Check the output panel for details.');
    } catch (error) {
        vscode.window.showErrorMessage(`Error applying code fixes: ${error}`);
    }
}

async function runGeneratedTests() {
    // This would integrate with the test execution functionality
    vscode.window.showInformationMessage('Test execution functionality would be implemented here.');
}

async function autoReviewDocument(document: vscode.TextDocument) {
    // Perform automatic code review when a document is saved
    vscode.window.showInformationMessage(`Auto-reviewing ${document.fileName}`);
    // Implementation would be similar to performCodeReview()
}