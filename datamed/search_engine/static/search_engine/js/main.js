new gridjs.Grid({
    columns: [
        {
            id: 'id_doc',
            name: 'PMID'
        },
        {
            id:'sentence_txt',
            name:'Текст предложения'
        },
        {
            id:'ddi_type',
            name:'Тип DDI'
        },
        {
            id: 'numb_sentence_in_doc',
            name:'Номер предложения в статье'
        },
        {
            name: 'Скачать статью',
            formatter: (_, row) =>
                gridjs.html(`<a href="https://sci-hub.ru/https://pubmed.ncbi.nlm.nih.gov/${row.cells[0].data}/" target="_blank">Скачать</a>`)
        },
    ],
    pagination: true,
    search: true,
    sort: true,
    resizable: true,
    data: list
}).render(document.getElementById("wrapper"));