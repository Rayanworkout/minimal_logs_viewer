let originalLogContent = '';
let isReversed = false;

document.getElementById('viewLogBtn').addEventListener('click', async () => {
    // Get selected project
    const project = document.getElementById('project').value;

    if (!project) {
        alert('Aucun projet sélectionné. Veuillez sélectionner un projet.');
        return;
    }

    try {
        // Send POST request to the API
        const response = await fetch('/get_logs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ project: project, as_df: false })
        });

        if (response.ok) {
            const data = await response.json();

            // Store the full log content
            originalLogContent = data.log_content;

            document.getElementById('logContent').value = originalLogContent;
        } else {
            alert("Impossible d'obtenir les logs de ce projet.");
        }
    } catch (error) {
        console.error('Error fetching logs:', error);
        alert('Une erreur est survenue.');
    }
});

document.getElementById('filterInput').addEventListener('input', filterLogs);
document.getElementById('failureFilter').addEventListener('change', filterLogs);

function filterLogs() {
    const filterText = document.getElementById('filterInput').value.toLowerCase();
    const showFailuresOnly = document.getElementById('failureFilter').checked;

    // Start with all logs
    let filteredLogs = originalLogContent.split('\n');

    // Apply text and failure filters if needed
    if (filterText || showFailuresOnly) {
        const keywords = filterText.split(/\s+/).filter(Boolean);

        filteredLogs = filteredLogs.filter(line => {
            const matchesText = keywords.every(keyword => line.toLowerCase().includes(keyword));
            const matchesFailure = !showFailuresOnly || line.toLowerCase().includes('failure');
            return matchesText && matchesFailure;
        });
    }

    if (isReversed) {
        filteredLogs = filteredLogs.reverse();
    }

    document.getElementById('logContent').value = filteredLogs.join('\n');
}


document.getElementById('reverseLogBtn').addEventListener('click', () => {
    isReversed = !isReversed;
    filterLogs();
});