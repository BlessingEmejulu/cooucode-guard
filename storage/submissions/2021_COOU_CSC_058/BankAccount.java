package edu.coou.banking;

public class BankAccount {
    private String accountNumber;
    private String accountHolder;
    private double balance;

    public BankAccount(String accountNumber, String accountHolder, double initialBalance) {
        this.accountNumber = accountNumber;
        this.accountHolder = accountHolder;
        this.balance = initialBalance;
    }

    public synchronized void deposit(double amount) {
        if (amount > 0) {
            this.balance += amount;
            System.out.println("Deposited: " + amount + ", New Balance: " + this.balance);
        }
    }

    public synchronized boolean withdraw(double amount) {
        if (amount > 0 && this.balance >= amount) {
            this.balance -= amount;
            System.out.println("Withdrew: " + amount + ", Remaining: " + this.balance);
            return true;
        }
        return false;
    }

    public double getBalance() {
        return this.balance;
    }
}
