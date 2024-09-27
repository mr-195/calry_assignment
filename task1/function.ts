function optimizeBookings(bookings: number[][]): number[][] {
    if (bookings.length === 0) return [];

    // sorting on the basis of start times
    bookings.sort((a, b) => a[0] - b[0]);

    const result: number[][] = [bookings[0]];

    for (let i = 1; i < bookings.length; i++) {
        const lastBooking = result[result.length - 1];
        const currentBooking = bookings[i];

        // if current one overlaps with the last one
        if (currentBooking[0] <= lastBooking[1]) {
            lastBooking[1] = Math.max(lastBooking[1], currentBooking[1]);
        } else {
            // if there is no overlap
            result.push(currentBooking);
        }
    }

    return result;
}


// Test cases

// #1 -> given
const bookings = [[9, 12], [11, 13], [14, 17], [16, 18]];
console.log(optimizeBookings(bookings));

// #2 -> non overlapping
const bookings1 = [[1, 3], [4, 5], [6, 8]];
console.log(optimizeBookings(bookings1));

// #3 consecutive bookings which touch each other from end to start
const bookings2 = [[1, 3], [3, 5], [5, 8]];
console.log(optimizeBookings(bookings2));

// #4 -> no overlap
const bookings3 = [[1, 2], [3, 4], [5, 6]];
console.log(optimizeBookings(bookings3));

// #5 empty
const bookings4: number[][] = [];
console.log(optimizeBookings(bookings4));