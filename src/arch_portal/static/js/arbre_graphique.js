

const width = 1200;
const height = 800;

const svg = d3.select("#tree-container")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(50,50)");

treeData.forEach((data, index) => {

    const root = d3.hierarchy(data);
    const treeLayout = d3.tree().size([height - 100, width - 200]);
    treeLayout(root);

    // Liens
    svg.selectAll(".link-" + index)
        .data(root.links())
        .enter()
        .append("line")
        .attr("x1", d => d.source.y)
        .attr("y1", d => d.source.x)
        .attr("x2", d => d.target.y)
        .attr("y2", d => d.target.x)
        .attr("stroke", "#999");

    // Noeuds
    const nodes = svg.selectAll(".node-" + index)
        .data(root.descendants())
        .enter()
        .append("g")
        .attr("transform", d => `translate(${d.y},${d.x})`);

    nodes.append("circle")
        .attr("r", 18)
        .attr("fill", "#0d6efd");

    nodes.append("text")
        .attr("dy", 5)
        .attr("x", 25)
        .text(d => d.data.name)
        .style("font-size", "13px");
});


function exportPDF() {
    const { jsPDF } = window.jspdf;

    html2canvas(document.querySelector("#tree-container")).then(canvas => {
        const imgData = canvas.toDataURL("image/png");

        const pdf = new jsPDF('landscape');
        pdf.addImage(imgData, 'PNG', 10, 10, 280, 180);
        pdf.save("arbre_famille.pdf");
    });
}

