// Collums for status
const statusColumns = ["Backlog", "In Progress", "QA", "Done"];

document.addEventListener("DOMContentLoaded", () => {
  // Update status
  statusColumns.forEach((status) => {
    const el = document.getElementById(status.replaceAll(" ", "_"));
    Sortable.create(el, {
      group: "tasks",
      animation: 150,
      onEnd: function (evt) {
        const taskId = evt.item.dataset.id;
        const newStatus = evt.to.dataset.status;
        fetch(`/update_status/${taskId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ status: newStatus }),
        });
      },
    });
  });

  // JS for adding tasks on a click for modal
  const cards = document.querySelectorAll(".task-card");
  cards.forEach((card) => {
    card.addEventListener("click", () => {
      const id = card.dataset.id;
      const title = card.dataset.title;
      const description = card.dataset.description;

      document.getElementById("editTaskId").value = id;
      document.getElementById("editTitle").value = title;
      document.getElementById("editDescription").value = description;
      document.getElementById("modalDeleteLink").href = `/delete/${id}`;
    });
  });


  // Search frontend
  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", () => {
    const term = searchInput.value.toLowerCase();
    document.querySelectorAll(".task-card").forEach((card) => {
      const title = card.dataset.title.toLowerCase();
      card.style.display = title.includes(term) ? "block" : "none";
    });
  });
});
