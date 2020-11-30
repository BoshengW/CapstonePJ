export class NewUser {
    private username: string;
    private email: string;
    private password: string;
    private birth: Date;

    constructor(username: string, email: string, password: string, birth: Date) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.birth = birth;

    }

    getUserName() {
        return this.username;
    }

    getEmail() {
        return this.email;
    }

    getPassword() {
        return this.password;
    }

    getBirth() {
        return this.birth;
    }
}
