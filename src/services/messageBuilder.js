function formatDueDate(isoDateString) {
  const date = new Date(isoDateString);
  if (Number.isNaN(date.getTime())) {
    return isoDateString || "-";
  }

  const pad = (value) => String(value).padStart(2, "0");
  const day = pad(date.getDate());
  const month = pad(date.getMonth() + 1);
  const year = date.getFullYear();
  const hour = pad(date.getHours());
  const minute = pad(date.getMinutes());

  return `${day}/${month}/${year} @ ${hour}:${minute}`;
}

function buildHomeworkMessage({ subject, title, detail, due }) {
  return [
    "📢 การบ้านใหม่มาแล้ว!",
    "━━━━━━━━━━━━━━",
    `📘 วิชา: ${subject || "-"}`,
    `📌 หัวข้อ: ${title || "-"}`,
    `📝 รายละเอียด: ${detail || "-"}`,
    `⏳ ส่งวันที่: ${formatDueDate(due)}`,
    "━━━━━━━━━━━━━━",
  ].join("\n");
}

module.exports = {
  buildHomeworkMessage,
};
