new gridjs.Grid({
    columns: [
        {
            id: 'text_before_bert',
            name: 'Текст до обработки',
        },
        {
            id:'text_after_bert',
            name:'Текст после обработки'
        },
        {
            id:'ddi',
            name:'Тип DDI'
        },
        {
            id:'sentence_number',
            name: 'Номер предложения'
        }
    ],
    pagination: true,
    search: true,
    sort: true,
    resizable: true,
    data: list
}).render(document.getElementById("wrapper"));