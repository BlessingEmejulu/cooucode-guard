package edu.coou.banking;

public class BankAccount {
    private String accId;
    private String clientName;
    private double currentFund;

    public BankAccount(String accId, String clientName, double startingAmount) {
        this.accId = accId;
        this.clientName = clientName;
        this.currentFund = startingAmount;
    }

    public synchronized void deposit(double cashIn) {
        if (cashIn > 0) {
            this.currentFund += cashIn;
            System.out.println("Credit: " + cashIn + ", Balance: " + this.currentFund);
        }
    }

    public synchronized boolean withdraw(double cashOut) {
        if (cashOut > 0 && this.currentFund >= cashOut) {
            this.currentFund -= cashOut;
            System.out.println("Debit: " + cashOut + ", Left: " + this.currentFund);
            return true;
        }
        return false;
    }

    public double getBalance() {
        return this.currentFund;
    }
}
