function getSeverity(ghs) {

    let score = 1;

    if (ghs.health.includes("Carcinogenic")) score = Math.max(score,5);

    if (ghs.health.includes("Toxic")) score = Math.max(score,4);

    if (ghs.health.includes("Corrosive")) score = Math.max(score,4);

    if (ghs.physical.includes("Flammable")) score = Math.max(score,3);

    if (ghs.health.includes("Irritant")) score = Math.max(score,2);

    return score;
}


function getExposure(quantity, environment) {

    let q = 1;
    let e = 1;

    if (quantity === "small") q = 1;
    if (quantity === "medium") q = 2;
    if (quantity === "large") q = 3;

    if (environment === "closed") e = 1;
    if (environment === "normal") e = 2;
    if (environment === "open") e = 3;

    return q + e;
}


function calculateRisk(chemical, quantity, environment) {

    const severity = getSeverity(chemical.ghs);

    const exposure = getExposure(quantity, environment);

    const risk = severity * exposure;

    let grade = "LOW";

    if (risk <= 4) grade = "LOW";
    else if (risk <= 9) grade = "MEDIUM";
    else if (risk <= 15) grade = "HIGH";
    else grade = "CRITICAL";

    return {
        severity: severity,
        exposure: exposure,
        risk: risk,
        grade: grade
    };
}