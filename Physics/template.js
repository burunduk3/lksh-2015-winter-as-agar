/**
 * While I didn't use any code from the original, it's a related program.
 * 
 * The entire field is 1200x1200
 */


// ----- Game Constants ----- \\
var FPS = 30;
var NUM_SKITTLES = 200;
var BOUND = 600; // It's assumed as [-BOUND, BOUND] by [-BOUND, BOUND].

// ----- Game Variables ----- \\
var colors = {
    // Basic Colors
    black: color(0, 0, 0),
    blue: color(0, 0, 255),
    green: color(0, 255, 0),
    cyan: color(0, 255, 255),
    red: color(255, 0, 0),
    pink: color(255, 0, 255),
    yellow: color(255, 255, 0),
    white: color(255, 255, 255),
    
    // Other Colors
    bg: color(221, 221, 160)
};
var showMass = true;
var primBlob; // Primary blob, it's the one centered on the screen.
var gameScroll = {
    x: 0,
    y: 0,
    handle: function() {
        this.x = width/2 - primBlob.pos.x;
        this.y = height/2 - primBlob.pos.y;
    }
};


// ---- Functions ----- \\

var thickText = function(txt, x, y, w, h) {
    for (var dx = -1; dx <= 1; dx++) {
        for (var dy = -1; dy <= 1; dy++) {
            var x2 = x + dx;
            var y2 = y + dy;
            if (arguments.length === 5) {
                text(txt, x2, y2, w, h);
            } else {
                text(txt, x2, y2);
            }
        }
    }
};


// ----- People have called those things "skittles", so ----- \\
var skittles = [];
var Skittle = function(x, y) {
    this.pos = new PVector(x, y);
    this.radius = 10;
    
    var colorList = ["white", "yellow", "green", "red", "blue", "pink"];
    var c = colorList[floor(random(0, colorList.length))];
    // gets the global colors object
    this.color = colors[c];
    
    this.type = ceil(random(5));
};
Skittle.prototype.draw = function() {
    fill(this.color);
    noStroke();
    if (this.type === 1) {
        // circle
        ellipse(this.pos.x, this.pos.y, this.radius * 2, this.radius * 2);
    } else {
        // create a polygon
        var sides = [5, 6, 8];
        var n = sides[this.type - 2];
        
        beginShape();
        for (var i = 0; i < n; i++) {
            var r = this.radius; // convinence
            vertex(this.pos.x + r * cos(i * 360 / n), this.pos.y + r * sin(i * 360 / n));
        }
        endShape(CLOSE);
    }
};

// ----- Handles the blobs ----- \\

var blobs = [];
var Blob = function(x, y, mass, color) {
    this.pos = new PVector(x, y);
    this.vel = new PVector(0, 0);
    this.accel = new PVector(0, 0);
    this.mass = mass;
    this.color = color;
    
    this.isPlayer = false;
    this.canEat = true;
    this.onEat = function () {};
    
    // The 10 is a scaling factor.
    Object.defineProperty(this, "radius", {
        get: function () {
            return sqrt(this.mass / PI) * 10;
        }
    });
};

Blob.prototype.move = function() {
    if (this.mass === 0) {return;}
    this.pos.add(PVector.div(this.vel, FPS));
    this.vel.add(PVector.div(this.accel, FPS));
    this.accel.mult(0);
};
Blob.prototype.applyForce = function(force) {
    if (this.mass === 0) {return;}
    this.accel.add(PVector.div(force, this.mass));
};

Blob.prototype.collideWith = function(that) {
    if (this.mass === 0) {return;}
    // Calculate the distance.
    var distanceBetween = PVector.sub(this.pos, that.pos).mag();
    if (distanceBetween < this.radius + that.radius) {
        // You need to be significantly bigger to eat them.
        if (this.mass > that.mass * 1.25) {
            this.mass += that.mass; // grow! grow! grow!
            that.mass = 0; // they're dead
        }
    }
};

Blob.prototype.eat = function(skittle) {
    if (!this.canEat) {return;}
    var dst = PVector.sub(this.pos, skittle.pos).mag();
    if (dst < this.radius + skittle.radius) {
        skittle.eaten = true;
        this.mass += 1;
    }
};

Blob.prototype.draw = function() {
    if (this.mass === 0) {return;}
    
    pushStyle();
    var fillColor = this.color;
    // make it 20% darker
    var strokeColor = lerpColor(this.color, colors.black, 0.2);
    // strokeWeight is obviously taken
    var strokeSize = this.radius * 0.2;
    var fillSize = this.radius - strokeSize/2;
    
    // draw this thing
    fill(fillColor);
    stroke(strokeColor);
    strokeWeight(strokeSize);
    ellipse(this.pos.x, this.pos.y, fillSize * 2, fillSize * 2);
    
    if (showMass) {
        fill(colors.black);
        textAlign(CENTER, CENTER);
        textSize(14);
        thickText(this.mass, this.pos.x, this.pos.y);
        fill(colors.white);
        text(this.mass, this.pos.x, this.pos.y);
    }
    
    popStyle();
};

// Your primary blob.
var primBlob = new Blob(0, 0, 10, colors.green);
primBlob.isPlayer = true;
blobs.push(primBlob);

// ----- INITIALIZATION ----- \\
// Initlaizes skittles.
var initSkittles = function(num) {
    for (var i = 0; i < num; i++) {
        var x = random(-1, 1) * BOUND;
        var y = random(-1, 1) * BOUND;
        skittles.push(new Skittle(x, y));
    }
};

initSkittles(NUM_SKITTLES);


// ----- GAME LOGIC ----- \\

var updatePlayer = function() {
    // Extract array of player blobs.
    var players = [];
    blobs.forEach(function(blob) {
        if (blob.isPlayer) {
            players.push(blob);
        }
    });
    
    var mouse = new PVector(mouseX - gameScroll.x, mouseY - gameScroll.y);
    
    // Now, move them towards your mouse
    players.forEach(function(blob) {
        var diff = PVector.sub(mouse, blob.pos);
        diff.limit(5000 / blob.radius);
        blob.vel = diff.get();
        
        // Move them
        blob.move();
        
        // Linear drag
        blob.vel.mult(0.9);
    });
};
var updateGame = function() {
    updatePlayer();
    
    blobs.forEach(function(blob) {
        if (!blob.isPlayer) {
            blob.move();
        }
    });
    
    // Since skittles are many, we can't afford to do more than one loop
    skittles.forEach(function(skit, index) {
        for (var i = 0; i < blobs.length; i++) {
            blobs[i].eat(skit);
            if (skit.eaten) {
                skittles.splice(index, 1);
                break;
            }
        }
    });
    gameScroll.handle();
};


// ----- RENDERING ----- \\

var renderGame = function() {
    gameScroll.handle();
    
    // Slowly zoom out as you collect mass
    var scl = 1 / (1 + primBlob.radius / 100);
    
    // Grid.
    stroke(0, 0, 0, 64);
    strokeWeight(1);
    var gSize = 50;
    var offX = ((gameScroll.x * scl) % gSize) - gSize;
    var offY = ((gameScroll.y * scl) % gSize) - gSize;
    var wdth = width / scl, hght = height / scl;
    for (offX; offX <= wdth; offX += gSize) {
        line(offX, 0, offX, hght);
    }
    for (offY; offY <= hght; offY += gSize) {
        line(0, offY, wdth, offY);
    }
    
    
    pushMatrix();
    translate(width/2, height/2);
    scale(scl);
    translate(-primBlob.pos.x, -primBlob.pos.y);
    
    // Draws all blobs and skittles.
    skittles.forEach(function(skit) {
        skit.draw();
    });
    blobs.forEach(function(blob) {
        blob.draw();
    });
    
    popMatrix();
    status(primBlob.pos);
};

keyPressed = function() {
    var k = key.toString().toLowerCase();
    if (k === "w") {
        var players = [];
        blobs.forEach(function(blob) {
            if (blob.isPlayer) {
                players.push(blob);
            }
        });
        var mouse = new PVector(mouseX - gameScroll.x, mouseY - gameScroll.y);
        players.forEach(function(p) {
            if (p.mass >= 36) {
                // throw towards mouse
                var diff = PVector.sub(mouse, p.pos);
                diff.normalize();
                diff.mult(600);
                var blob = new Blob(p.pos.x, p.pos.y, 18, p.color);
                blob.canEat = false;
                blob.vel = diff;
                blob.move();
                blobs.push(blob);
                
                p.mass -= 20;
            }
        });
    }
};

mouseX = width/2;
mouseY = height/2;
var draw = function() {
    background(221, 221, 160);
    updateGame();
    renderGame();
};
