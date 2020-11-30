export class Movie {
    private moviename: string;
    private rate: number;

    constructor(moviename: string, rate: number) {
        this.moviename = moviename;
        this.rate = rate;

    }

    getMovieName() {
        return this.moviename;
    }

    getRate() {
        return this.rate;
    }


}
