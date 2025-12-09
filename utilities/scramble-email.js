#!/usr/bin/env node

/**
 * Utility to generate scrambled email addresses
 * Usage: node scramble-email.js your.email@example.com
 */

function scrambleEmail(email) {
  if (!email || typeof email !== "string") {
    return "";
  }

  const chars = email.split("");
  const len = email.length;

  for (let i = 0; i < len - 1; i++) {
    const swapTarget = (i + len) % (len - i);
    const j = i + swapTarget;
    [chars[i], chars[j]] = [chars[j], chars[i]];
  }

  return chars.join("");
}

// Get email from command line arguments
const email = process.argv[2];

if (!email) {
  console.error("Usage: node scramble-email.js your.email@example.com");
  process.exit(1);
}

const scrambled = scrambleEmail(email);

console.log("\n" + "=".repeat(50));
console.log("Email Scrambler Utility");
console.log("=".repeat(50));
console.log(`\nOriginal email: ${email}`);
console.log(`Scrambled email: ${scrambled}`);
console.log(`\nLength: ${email.length} characters`);
console.log("\nUse this scrambled version in your contact page.");
console.log("=".repeat(50) + "\n");
