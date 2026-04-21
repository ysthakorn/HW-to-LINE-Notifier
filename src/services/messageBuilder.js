function parseDateValue(input) {
  if (!input) {
    return null;
  }

  const directDate = new Date(input);
  if (!Number.isNaN(directDate.getTime())) {
    return directDate;
  }

  const trimmed = String(input).trim();
  const match = trimmed.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})(?:\s+(\d{1,2}):(\d{2}))?$/);
  if (!match) {
    return null;
  }

  const day = Number(match[1]);
  const month = Number(match[2]);
  let year = Number(match[3]);
  const hours = Number(match[4] || 0);
  const minutes = Number(match[5] || 0);

  if (year > 2400) {
    year -= 543;
  }

  const parsed = new Date(year, month - 1, day, hours, minutes);
  if (Number.isNaN(parsed.getTime())) {
    return null;
  }

  return parsed;
}

function formatDueDate(dateString) {
  const date = parseDateValue(dateString);
  if (!date) {
    return dateString || "-";
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
  formatDueDate,
};
