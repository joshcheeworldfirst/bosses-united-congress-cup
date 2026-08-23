/**
 * Congress Cup Opening Ceremony — registration endpoint.
 *
 * Receives the form POST from the registration page and appends one row to the
 * 26 Aug tab of "Bosses United x WorldFirst Event Registration".
 *
 * A Google Form can only write to the response tab it owns, which is why this
 * exists: it lets rows land in a specific, pre-made tab (TAB_GID below).
 *
 * DEPLOY
 *   1. Open the spreadsheet → Extensions → Apps Script.
 *   2. Replace the default Code.gs with this file, and Save.
 *   3. Deploy → New deployment → type "Web app".
 *        Execute as:      Me
 *        Who has access:  Anyone
 *   4. Authorise when prompted, then copy the Web app URL (ends in /exec).
 *   5. Paste that URL into RSVP.ENDPOINT in the page's registration script.
 *
 * Re-deploying after an edit: Deploy → Manage deployments → edit → New version.
 * (A new *deployment* gets a new URL; a new *version* keeps the same one.)
 *
 * Note: "Who has access: Anyone" makes the URL a public write endpoint — the
 * same exposure a public Google Form has. It only ever appends to this one tab.
 */

var SHEET_ID = '1O_3FNDM6yrcbw2Qa7ERwdMB6DZVIwf2Ns0rcN9EC1-w';
var TAB_GID = 1478474401;

var HEADERS = [
  'Timestamp',
  'First and last name',
  'Company name',
  'Email',
  'Mobile number (with country code. Eg 6591234567)',
  'Industry',
  'By ticking this box and registering for this event, you consent to receiving ' +
    'post-event communications from participating organisations'
];

function doPost(e) {
  var p = (e && e.parameter) || {};

  // Minimum viable submission — anything less is a malformed or bot post.
  if (!p.name || !p.email) {
    return reply('Missing name or email.');
  }

  var sheet = tabByGid_(SHEET_ID, TAB_GID);
  if (!sheet) {
    return reply('No tab with gid ' + TAB_GID + ' in that spreadsheet.');
  }

  // Serialise appends so two simultaneous submissions cannot claim one row.
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
  } catch (err) {
    return reply('Busy, please retry.');
  }

  try {
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
      sheet.setFrozenRows(1);
    }
    sheet.appendRow([
      new Date(),
      trim_(p.name),
      trim_(p.company),
      trim_(p.email),
      // leading apostrophe keeps "+65..." and leading zeros as text, not a number
      "'" + trim_(p.mobile),
      trim_(p.industry),
      trim_(p.consent)
    ]);
  } finally {
    lock.releaseLock();
  }

  return reply('Recorded.');
}

/** Lets you confirm the deployment is live by opening the /exec URL. */
function doGet() {
  var sheet = tabByGid_(SHEET_ID, TAB_GID);
  return reply(sheet
    ? 'Registration endpoint is live. Target tab: "' + sheet.getName() + '".'
    : 'Endpoint is live, but no tab with gid ' + TAB_GID + ' was found.');
}

function tabByGid_(id, gid) {
  var sheets = SpreadsheetApp.openById(id).getSheets();
  for (var i = 0; i < sheets.length; i++) {
    if (sheets[i].getSheetId() === gid) return sheets[i];
  }
  return null;
}

function trim_(v) {
  return v == null ? '' : String(v).trim();
}

/**
 * The page posts into a hidden iframe and treats the iframe's load event as
 * success, so the response must be framable — hence ALLOWALL.
 */
function reply(message) {
  return HtmlService
    .createHtmlOutput('<!doctype html><meta charset="utf-8"><p>' + message + '</p>')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
